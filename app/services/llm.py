import os
import httpx
import json
from typing import AsyncGenerator
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")
HTTP_PROXY = os.getenv("HTTP_PROXY", os.getenv("http_proxy", ""))
HTTPS_PROXY = os.getenv("HTTPS_PROXY", os.getenv("https_proxy", ""))

def _get_proxy():
    # httpx >= 0.28.0 uses 'proxy' not 'proxies'
    if HTTPS_PROXY:
        return HTTPS_PROXY
    if HTTP_PROXY:
        return HTTP_PROXY
    return None

async def _call_llm(messages: list, max_tokens: int = 1500) -> str:
    if not OPENAI_API_KEY:
        return "MOCK_LLM_RESPONSE: " + messages[-1]["content"][:100] + "..."

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.2
    }

    client_args = {"timeout": 30.0}
    proxy = _get_proxy()
    if proxy:
        client_args["proxy"] = proxy

    try:
        async with httpx.AsyncClient(**client_args) as client:
            response = await client.post(
                f"{OPENAI_API_BASE}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"LLM Error: {e}")
        return f"Fehler bei der LLM-Abfrage: {e}"

async def _call_llm_stream(messages: list, max_tokens: int = 1500) -> AsyncGenerator[str, None]:
    if not OPENAI_API_KEY:
        mock_response = "MOCK_LLM_RESPONSE: " + messages[-1]["content"][:50] + "..."
        for word in mock_response.split():
            yield word + " "
        return

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "stream": True
    }

    client_args = {"timeout": 30.0}
    proxy = _get_proxy()
    if proxy:
        client_args["proxy"] = proxy

    try:
        async with httpx.AsyncClient(**client_args) as client:
            async with client.stream(
                "POST",
                f"{OPENAI_API_BASE}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        try:
                            data = json.loads(line[6:])
                            delta = data["choices"][0].get("delta", {}).get("content", "")
                            if delta:
                                yield delta
                        except json.JSONDecodeError:
                            continue
    except Exception as e:
        print(f"LLM Stream Error: {e}")
        yield f"Fehler bei der LLM-Abfrage: {e}"

async def generate_essenz(text: str) -> str:
    messages = [
        {"role": "system", "content": "Du bist ein erfahrener Analyst. Fasse das folgende Dokument präzise zusammen. Extrahiere die Essenz: Kernaussagen, Sachverhalt, Risiken und Handlungsimplikationen."},
        {"role": "user", "content": text}
    ]
    return await _call_llm(messages)

async def generate_index(text: str) -> str:
    messages = [
        {"role": "system", "content": "Du bist ein strukturierter Archivar. Erstelle aus dem folgenden Text einen kompakten Index (Gegenstand, Beteiligte, relevante Zeitpunkte, Fristen, Risiken, Konflikte). Antworte in einer übersichtlichen Struktur."},
        {"role": "user", "content": text}
    ]
    return await _call_llm(messages)

async def chat_with_document_stream(document_text: str, essenz: str, user_query: str) -> AsyncGenerator[str, None]:
    messages = [
        {"role": "system", "content": f"Du bist Raz_Sof, ein agentischer Assistent für die Analyse von Dokumenten. Du bist präzise, professionell und analytisch.\n\nKontext des Dokuments (Essenz):\n{essenz}\n\nVollständiger Text:\n{document_text}\n\nBeantworte die Fragen des Nutzers basierend auf diesem Dokument."},
        {"role": "user", "content": user_query}
    ]
    async for chunk in _call_llm_stream(messages):
        yield chunk
