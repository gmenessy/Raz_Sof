from sqlalchemy import text
from app.database import engine, Base, SessionLocal
from app.models.models import Mandant, Nutzer, Akte

def init_db():
    # If using postgres, ensure vector extension is enabled
    if engine.url.drivername in ['postgres', 'postgresql', 'postgresql+psycopg2']:
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Create default tenant and user for MVP
    default_mandant = db.query(Mandant).filter(Mandant.name == "Raz_Sof_Default").first()
    if not default_mandant:
        default_mandant = Mandant(name="Raz_Sof_Default")
        db.add(default_mandant)
        db.commit()
        db.refresh(default_mandant)

    default_nutzer = db.query(Nutzer).filter(Nutzer.username == "admin").first()
    if not default_nutzer:
        default_nutzer = Nutzer(username="admin", mandant_id=default_mandant.id)
        db.add(default_nutzer)
        db.commit()

    default_akte = db.query(Akte).filter(Akte.titel == "Allgemeine Akte").first()
    if not default_akte:
        default_akte = Akte(titel="Allgemeine Akte", mandant_id=default_mandant.id)
        db.add(default_akte)
        db.commit()

    db.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
