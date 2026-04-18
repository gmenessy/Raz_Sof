import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")

def _call_llm(messages: list, max_tokens: int = 1500) -> str:
    if not OPENAI_API_KEY:
        # Mock response if no key is provided
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

    try:
        response = requests.post(
            f"{OPENAI_API_BASE}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"LLM Error: {e}")
        return f"Fehler bei der LLM-Abfrage: {e}"

def generate_essenz(text: str) -> str:
    messages = [
        {"role": "system", "content": "Du bist ein erfahrener Analyst. Fasse das folgende Dokument präzise zusammen. Extrahiere die Essenz: Kernaussagen, Sachverhalt, Risiken und Handlungsimplikationen."},
        {"role": "user", "content": text}
    ]
    return _call_llm(messages)

def generate_index(text: str) -> str:
    messages = [
        {"role": "system", "content": "Du bist ein strukturierter Archivar. Erstelle aus dem folgenden Text einen kompakten Index (Gegenstand, Beteiligte, relevante Zeitpunkte, Fristen, Risiken, Konflikte). Antworte in einer übersichtlichen Struktur."},
        {"role": "user", "content": text}
    ]
    return _call_llm(messages)

def chat_with_document(document_text: str, essenz: str, user_query: str) -> str:
    messages = [
        {"role": "system", "content": f"Du bist Raz_Sof, ein agentischer Assistent für die Analyse von Dokumenten. Du bist präzise, professionell und analytisch.\n\nKontext des Dokuments (Essenz):\n{essenz}\n\nVollständiger Text:\n{document_text}\n\nBeantworte die Fragen des Nutzers basierend auf diesem Dokument."},
        {"role": "user", "content": user_query}
    ]
    return _call_llm(messages)
