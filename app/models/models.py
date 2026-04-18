from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Mandant(Base):
    __tablename__ = "mandanten"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    nutzer = relationship("Nutzer", back_populates="mandant")
    akten = relationship("Akte", back_populates="mandant")

class Nutzer(Base):
    __tablename__ = "nutzer"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    mandant_id = Column(Integer, ForeignKey("mandanten.id"))

    mandant = relationship("Mandant", back_populates="nutzer")

class Akte(Base):
    __tablename__ = "akten"

    id = Column(Integer, primary_key=True, index=True)
    titel = Column(String, index=True)
    status = Column(String, default="aktiv") # aktiv / archiviert
    mandant_id = Column(Integer, ForeignKey("mandanten.id"))

    mandant = relationship("Mandant", back_populates="akten")
    dokumente = relationship("Dokument", back_populates="akte")

class Dokument(Base):
    __tablename__ = "dokumente"

    id = Column(Integer, primary_key=True, index=True)
    dateiname = Column(String)
    inhalt = Column(Text) # Raw text extracted from file
    essenz = Column(Text, nullable=True) # Summary / Essenz
    index_data = Column(Text, nullable=True) # JSON or structured text for Index
    akte_id = Column(Integer, ForeignKey("akten.id"))
    hochgeladen_am = Column(DateTime, default=datetime.utcnow)

    akte = relationship("Akte", back_populates="dokumente")
