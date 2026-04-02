"""
database.py — Connexion base de données
Dev  : SQLite (zéro config, fichier local)
Prod : PostgreSQL sur Railway (changer DATABASE_URL dans .env)
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# SQLite en dev, PostgreSQL en prod
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./link2job.db")

# SQLite a besoin de check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ── MODÈLES ─────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    email         = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name     = Column(String, nullable=True)
    is_active     = Column(Boolean, default=True)
    plan          = Column(String, default="free")      # free | candidat | pro
    analyses_used = Column(Integer, default=0)          # compteur analyses gratuites
    created_at    = Column(DateTime, default=datetime.utcnow)


class Analysis(Base):
    __tablename__ = "analyses"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, nullable=False)
    linkedin_url   = Column(String, nullable=True)
    score_before   = Column(Integer, nullable=True)
    score_details  = Column(String, nullable=True)   # JSON stringifié
    created_at     = Column(DateTime, default=datetime.utcnow)


# ── INIT DB ─────────────────────────────────────────────────────────

def init_db():
    """Crée toutes les tables si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)


# ── DEPENDENCY ──────────────────────────────────────────────────────

def get_db():
    """FastAPI dependency — session DB par requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()