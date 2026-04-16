"""
auth.py — Authentification Link2Job
- Inscription email + mot de passe
- Connexion → JWT token
- Middleware current_user
- Compteur 3 analyses gratuites
- Compteur 3 posts gratuits/mois
"""
import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database import get_db, User

# ── CONFIG ──────────────────────────────────────────────────────────
SECRET_KEY        = os.getenv("SECRET_KEY", "link2job-dev-secret-change-in-prod")
ALGORITHM         = "HS256"
TOKEN_EXPIRE_DAYS = 30
FREE_ANALYSES_LIMIT = 3
FREE_POSTS_LIMIT    = 3   # 3 posts gratuits par mois

pwd_context  = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ── SCHEMAS ─────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserPublic(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    plan: str
    analyses_used: int
    analyses_remaining: int
    posts_used: int
    posts_remaining: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── HELPERS ─────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def _analyses_remaining(user: User) -> int:
    if user.plan != "free":
        return 999  # illimité
    return max(0, FREE_ANALYSES_LIMIT - user.analyses_used)

def _check_and_reset_posts(user: User, db: Session) -> None:
    """Reset le compteur posts si on est dans un nouveau mois calendaire."""
    now = datetime.utcnow()
    reset_date = user.posts_reset_date or datetime.utcnow()

    # Nouveau mois = reset
    if now.year > reset_date.year or now.month > reset_date.month:
        user.posts_used = 0
        user.posts_reset_date = now
        db.commit()

def _posts_remaining(user: User) -> int:
    """Retourne le nombre de posts restants ce mois-ci."""
    if user.plan != "free":
        return 999  # illimité
    posts_used = user.posts_used or 0
    return max(0, FREE_POSTS_LIMIT - posts_used)


# ── DEPENDENCY current_user ──────────────────────────────────────────

async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Retourne l'utilisateur connecté ou None si pas de token."""
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        return None
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()


async def require_user(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """Retourne l'utilisateur connecté ou lève une 401."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Connecte-toi pour continuer.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


# ── ROUTES ──────────────────────────────────────────────────────────

def _user_dict(user: User) -> dict:
    """Construit le dict user renvoyé au frontend."""
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "plan": user.plan,
        "analyses_used": user.analyses_used,
        "analyses_remaining": _analyses_remaining(user),
        "posts_used": user.posts_used or 0,
        "posts_remaining": _posts_remaining(user),
    }


@router.post("/register", response_model=LoginResponse)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """Inscription — crée un compte et retourne un token JWT."""
    existing = db.query(User).filter(User.email == body.email.lower().strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")
    if len(body.password) < 8:
        raise HTTPException(status_code=400, detail="Le mot de passe doit faire au moins 8 caractères.")

    user = User(
        email=body.email.lower().strip(),
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id)
    return LoginResponse(access_token=token, user=_user_dict(user))


@router.post("/login", response_model=LoginResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Connexion — retourne un token JWT."""
    user = db.query(User).filter(User.email == form.username.lower().strip()).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Compte désactivé.")

    token = create_token(user.id)
    return LoginResponse(access_token=token, user=_user_dict(user))


@router.get("/me")
def me(current_user: User = Depends(require_user)):
    """Retourne le profil de l'utilisateur connecté."""
    return _user_dict(current_user)