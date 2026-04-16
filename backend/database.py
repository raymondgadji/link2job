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

    id               = Column(Integer, primary_key=True, index=True)
    email            = Column(String, unique=True, index=True, nullable=False)
    hashed_password  = Column(String, nullable=False)
    full_name        = Column(String, nullable=True)
    is_active        = Column(Boolean, default=True)
    plan             = Column(String, default="free")      # free | candidat | pro
    analyses_used    = Column(Integer, default=0)          # compteur analyses gratuites
    posts_used       = Column(Integer, default=0)          # compteur posts ce mois-ci
    posts_reset_date = Column(DateTime, default=datetime.utcnow)  # date du dernier reset
    created_at       = Column(DateTime, default=datetime.utcnow)


class Analysis(Base):
    __tablename__ = "analyses"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, nullable=False)
    linkedin_url   = Column(String, nullable=True)
    score_before   = Column(Integer, nullable=True)
    score_details  = Column(String, nullable=True)   # JSON stringifié
    created_at     = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    __tablename__ = "posts"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, nullable=False, index=True)
    idee       = Column(String, nullable=True)        # L'idée brute de l'utilisateur
    ton        = Column(String, nullable=True)         # tous | inspirant | expert | authentique
    secteur    = Column(String, nullable=True)
    contenu    = Column(String, nullable=True)         # JSON stringifié des 3 posts
    created_at = Column(DateTime, default=datetime.utcnow)


# ── INIT DB ─────────────────────────────────────────────────────────

def init_db():
    """Crée toutes les tables si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)

    # Migration douce : ajoute les colonnes si elles n'existent pas (SQLite + PostgreSQL)
    from sqlalchemy import text, inspect
    inspector = inspect(engine)
    columns = [col["name"] for col in inspector.get_columns("users")]

    with engine.connect() as conn:
        if "posts_used" not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN posts_used INTEGER DEFAULT 0"))
            conn.commit()
        if "posts_reset_date" not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN posts_reset_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
            conn.commit()


# ── DEPENDENCY ──────────────────────────────────────────────────────

def get_db():
    """FastAPI dependency — session DB par requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()