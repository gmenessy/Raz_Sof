import os
import httpx
import tiktoken
from typing import List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
HTTP_PROXY = os.getenv("HTTP_PROXY", os.getenv("http_proxy", ""))
HTTPS_PROXY = os.getenv("HTTPS_PROXY", os.getenv("https_proxy", ""))

def _get_proxy():
    if HTTPS_PROXY:
        return HTTPS_PROXY
    if HTTP_PROXY:
        return HTTP_PROXY
    return None

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Splits text into chunks of roughly `chunk_size` tokens using tiktoken."""
    try:
        enc = tiktoken.encoding_for_model("gpt-4o") # defaults to o200k_base or cl100k_base
    except Exception:
        enc = tiktoken.get_encoding("cl100k_base")

    tokens = enc.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunks.append(enc.decode(chunk_tokens))
        start += chunk_size - overlap

    return chunks

async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Fetches embeddings for a list of text chunks from the OpenAI API."""
    if not OPENAI_API_KEY:
        # Return mock embeddings (1536 zeros) if no key is provided
        return [[0.0] * 1536 for _ in texts]

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-embedding-ada-002",
        "input": texts
    }

    client_args = {"timeout": 60.0}
    proxy = _get_proxy()
    if proxy:
        client_args["proxy"] = proxy

    try:
        async with httpx.AsyncClient(**client_args) as client:
            response = await client.post(
                f"{OPENAI_API_BASE}/embeddings",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            # The API returns objects in the same order as the input texts
            embeddings = [item["embedding"] for item in data["data"]]
            return embeddings
    except Exception as e:
        print(f"Embedding Error: {e}")
        return []
