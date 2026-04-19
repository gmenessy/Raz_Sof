from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
import io
import PyPDF2

from app.database import get_db, SessionLocal
from app.models.models import Dokument, Akte, Mandant, DokumentChunk
from app.services.llm import generate_essenz, generate_index, chat_with_document_stream
from app.services.rag import chunk_text, get_embeddings
import asyncio

router = APIRouter(prefix="/api")

class ChatRequest(BaseModel):
    dokument_id: int
    message: str

class DokumentResponse(BaseModel):
    id: int
    dateiname: str
    essenz: str | None
    index_data: str | None

    class Config:
        from_attributes = True

async def analyze_document_task(dokument_id: int, text_content: str):
    """Background task to analyze the document using LLM and create RAG chunks."""
    db = SessionLocal()
    try:
        # 1. Generate Summaries (Essenz & Index)
        essenz = await generate_essenz(text_content[:10000])
        index_data = await generate_index(text_content[:10000])

        dok = db.query(Dokument).filter(Dokument.id == dokument_id).first()
        if dok:
            dok.essenz = essenz
            dok.index_data = index_data

            # 2. Process Vector Chunks for RAG
            chunks = chunk_text(text_content)
            if chunks:
                embeddings = await get_embeddings(chunks)

                # Verify we got valid embeddings back
                if embeddings and len(embeddings) == len(chunks):
                    for idx, chunk_text_str in enumerate(chunks):
                        db_chunk = DokumentChunk(
                            dokument_id=dok.id,
                            text_content=chunk_text_str,
                            embedding=embeddings[idx]
                        )
                        db.add(db_chunk)

            db.commit()
    except Exception as e:
        print(f"Error in background task: {e}")
        db.rollback()
    finally:
        db.close()


@router.post("/upload", response_model=DokumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    akte_id: int = Form(...),
    db: Session = Depends(get_db)
):
    akte = db.query(Akte).filter(Akte.id == akte_id).first()
    if not akte:
        raise HTTPException(status_code=404, detail="Akte nicht gefunden")

    content = await file.read()

    text = ""
    if file.filename.lower().endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            text = "Fehler beim Lesen der PDF."
    else:
        text = content.decode("utf-8", errors="ignore")

    dok = Dokument(
        dateiname=file.filename,
        inhalt=text,
        essenz=None,
        index_data=None,
        akte_id=akte.id
    )
    db.add(dok)
    db.commit()
    db.refresh(dok)

    background_tasks.add_task(analyze_document_task, dok.id, text)

    return dok

@router.get("/akten", response_model=List[dict])
def get_akten(db: Session = Depends(get_db)):
    akten = db.query(Akte).all()
    result = []
    for a in akten:
        docs = db.query(Dokument).filter(Dokument.akte_id == a.id).all()
        result.append({
            "id": a.id,
            "titel": a.titel,
            "status": a.status,
            "dokumente": [{"id": d.id, "dateiname": d.dateiname, "essenz": d.essenz, "index_data": d.index_data} for d in docs]
        })
    return result

@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    dok = db.query(Dokument).filter(Dokument.id == request.dokument_id).first()
    if not dok:
        raise HTTPException(status_code=404, detail="Dokument nicht gefunden")

    # Attempt to do vector search to find relevant context instead of just reading first 10k chars
    relevant_context = ""
    try:
        # Embed the user query
        query_embeddings = await get_embeddings([request.message])
        if query_embeddings and len(query_embeddings[0]) == 1536:
            query_vector = query_embeddings[0]
            # Use pgvector cosine distance to find top 5 chunks
            top_chunks = db.scalars(
                select(DokumentChunk)
                .filter(DokumentChunk.dokument_id == dok.id)
                .order_by(DokumentChunk.embedding.cosine_distance(query_vector))
                .limit(5)
            ).all()

            if top_chunks:
                relevant_context = "\n\n---\n\n".join([c.text_content for c in top_chunks])
    except Exception as e:
        print(f"Error during vector search: {e}")

    # Fallback to the old logic if vector search yields nothing (e.g. no key, sqlite mode, etc)
    if not relevant_context:
        relevant_context = dok.inhalt[:10000]

    async def event_generator():
        async for chunk in chat_with_document_stream(
            document_text=relevant_context,
            essenz=dok.essenz or "",
            user_query=request.message
        ):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")
