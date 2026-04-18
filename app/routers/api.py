from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.models.models import Dokument, Akte, Mandant
from app.services.llm import generate_essenz, generate_index, chat_with_document

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

@router.post("/upload", response_model=DokumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    akte_id: int = Form(...),
    db: Session = Depends(get_db)
):
    akte = db.query(Akte).filter(Akte.id == akte_id).first()
    if not akte:
        raise HTTPException(status_code=404, detail="Akte nicht gefunden")

    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    # Analyze with LLM
    essenz = generate_essenz(text[:10000]) # simple limit to avoid huge payload in MVP
    index_data = generate_index(text[:10000])

    dok = Dokument(
        dateiname=file.filename,
        inhalt=text,
        essenz=essenz,
        index_data=index_data,
        akte_id=akte.id
    )
    db.add(dok)
    db.commit()
    db.refresh(dok)

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
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    dok = db.query(Dokument).filter(Dokument.id == request.dokument_id).first()
    if not dok:
        raise HTTPException(status_code=404, detail="Dokument nicht gefunden")

    response_text = chat_with_document(
        document_text=dok.inhalt[:10000],
        essenz=dok.essenz or "",
        user_query=request.message
    )

    return {"response": response_text}
