from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import get_db, SessionLocal
from app.models.models import Dokument, Akte, Mandant
from app.services.llm import generate_essenz, generate_index, chat_with_document
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
    """Background task to analyze the document using LLM"""
    # Use a new DB session for the background task
    db = SessionLocal()
    try:
        # LLM Calls
        essenz = await generate_essenz(text_content[:10000])
        index_data = await generate_index(text_content[:10000])

        # Update Database
        dok = db.query(Dokument).filter(Dokument.id == dokument_id).first()
        if dok:
            dok.essenz = essenz
            dok.index_data = index_data
            db.commit()
    except Exception as e:
        print(f"Error in background task: {e}")
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
    text = content.decode("utf-8", errors="ignore")

    # Save the document immediately with empty essenz/index
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

    # Queue background processing
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

    response_text = await chat_with_document(
        document_text=dok.inhalt[:10000],
        essenz=dok.essenz or "",
        user_query=request.message
    )

    return {"response": response_text}
