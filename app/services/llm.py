import os
import httpx
import json
import re
from typing import AsyncGenerator
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")
HTTP_PROXY = os.getenv("HTTP_PROXY", os.getenv("http_proxy", ""))
HTTPS_PROXY = os.getenv("HTTPS_PROXY", os.getenv("https_proxy", ""))

def _get_proxy():
    if HTTPS_PROXY:
        return HTTPS_PROXY
    if HTTP_PROXY:
        return HTTP_PROXY
    return None

async def _call_llm(messages: list, max_tokens: int = 1500, temperature: float = 0.2) -> str:
    if not OPENAI_API_KEY:
        if "JSON-Array" in messages[0]["content"]:
             return '["advocatus_diaboli", "anforderungs_analyse", "kosten_detektiv"]'
        return "MOCK_LLM_RESPONSE: " + messages[-1]["content"][:100] + "..."

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
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

async def chat_with_document_stream(document_text: str, essenz: str, user_query: str, skill_prompt: str = None) -> AsyncGenerator[str, None]:
    base_sys_prompt = "Du bist Raz_Sof, ein agentischer Assistent für die Analyse von Dokumenten. Du bist präzise, professionell und analytisch."

    if skill_prompt:
        base_sys_prompt += f"\n\nWENDE FOLGENDEN SKILL AN:\n{skill_prompt}"

    messages = [
        {"role": "system", "content": f"{base_sys_prompt}\n\nKontext des Dokuments (Essenz):\n{essenz}\n\nVollständiger Text (bzw. relevante Chunks):\n{document_text}\n\nBeantworte die Fragen des Nutzers basierend auf diesem Dokument und der Skill-Anweisung."},
        {"role": "user", "content": user_query}
    ]
    async for chunk in _call_llm_stream(messages):
        yield chunk

async def discover_relevant_skills(essenz: str, query: str, available_skills: list) -> list:
    """Uses the LLM to suggest the top 3 skill IDs based on the document summary and user query."""

    skills_json = json.dumps([{"id": s["id"], "name": s["name"], "ziel": s["ziel"]} for s in available_skills], ensure_ascii=False)

    sys_prompt = f"""Du bist ein Router-Agent für Raz_Sof. Deine Aufgabe ist es, basierend auf dem Kontext des Dokuments und der Nutzeranfrage die 3 passendsten Analyse-Skills auszuwählen.

Hier ist die Liste der verfügbaren Skills (als JSON):
{skills_json}

Antworte AUSSCHLIESSLICH mit einem JSON-Array, das die 3 besten Skill-IDs als Strings enthält. Beispiel: ["advocatus_diaboli", "prozess_chirurg", "echo_filter"]
Kein Markdown, kein Text davor oder danach."""

    user_prompt = f"Dokumenten-Essenz:\n{essenz}\n\nNutzer-Anfrage:\n{query}"

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response_text = await _call_llm(messages, max_tokens=100, temperature=0.0)
        # Parse the JSON array
        # Clean potential markdown formatting if the model disobeys

        # Use regex to find the first array structure in case there's text around it
        match = re.search(r'\[.*\]', response_text.replace('\n', ' '))
        if match:
            response_text = match.group(0)

        skill_ids = json.loads(response_text)
        if isinstance(skill_ids, list):
            return [s for s in skill_ids if isinstance(s, str)][:3]
        return []
    except Exception as e:
        print(f"Error discovering skills: {e}")
        # Fallback to default skills if parsing fails or offline
        return ["advocatus_diaboli", "anforderungs_analyse", "kosten_detektiv"]
