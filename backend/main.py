from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import json

from database import get_db, init_db, Analysis, Post, User
from auth import router as auth_router, get_current_user, require_user, _analyses_remaining, _posts_remaining, _check_and_reset_posts, FREE_ANALYSES_LIMIT, FREE_POSTS_LIMIT
from stripe_router import router as stripe_router
from utils.linkedin_parser import parse_linkedin_profile
from utils.ai_agent import analyze_profile, create_profile_from_scratch, generate_linkedin_post
from utils.scorer import compute_score

app = FastAPI(title="Link2Job API", version="0.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(auth_router)
app.include_router(stripe_router)

# ── MODÈLES ────────────────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    linkedin_url: str

class AnalyzeResponse(BaseModel):
    score_before: int
    score_details: dict
    recommendations: dict
    optimized_texts: dict
    analyses_remaining: Optional[int] = None
    analyses_used: Optional[int] = None

class CreateProfileRequest(BaseModel):
    prenom: str
    nom: Optional[str] = ""
    secteur: str
    niveau: str
    ville: Optional[str] = ""
    experiences: Optional[list] = []
    hard_skills: Optional[list] = []
    soft_skills: Optional[list] = []
    langues: Optional[str] = ""
    contrat: str
    poste_vise: Optional[str] = ""
    infos_sup: Optional[str] = ""

class GeneratePostRequest(BaseModel):
    idee: str                          # L'idée brute de l'utilisateur
    ton: Optional[str] = "tous"        # inspirant | expert | authentique | tous
    secteur: Optional[str] = ""        # Auto-rempli depuis le profil
    poste: Optional[str] = ""          # Poste visé

# ── ENDPOINTS ──────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.4.0"}


@app.post("/api/analyze-profile", response_model=AnalyzeResponse)
async def analyze_profile_route(
    body: AnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    is_demo = current_user is None

    if not is_demo:
        remaining = _analyses_remaining(current_user)
        if remaining <= 0:
            raise HTTPException(
                status_code=403,
                detail="Tu as utilisé tes 3 analyses gratuites. Passe au plan Candidat pour continuer. 🚀"
            )

    profile_data = await parse_linkedin_profile(body.linkedin_url)
    if not profile_data:
        raise HTTPException(
            status_code=422,
            detail="L'analyse directe depuis URL est temporairement désactivée. Utilise le formulaire guidé pour créer ton profil LinkedIn optimisé. 👉 create-profile.html"
        )

    score_details = compute_score(profile_data)
    ai_result = await analyze_profile(profile_data, score_details)

    if not is_demo:
        current_user.analyses_used += 1
        analysis = Analysis(
            user_id=current_user.id,
            linkedin_url=body.linkedin_url,
            score_before=score_details["total"],
            score_details=json.dumps(score_details),
        )
        db.add(analysis)
        db.commit()
        db.refresh(current_user)

    return AnalyzeResponse(
        score_before=score_details["total"],
        score_details=score_details,
        recommendations=ai_result["recommendations"],
        optimized_texts=ai_result["optimized_texts"],
        analyses_remaining=_analyses_remaining(current_user) if not is_demo else None,
        analyses_used=current_user.analyses_used if not is_demo else None,
    )


@app.get("/api/my-analyses")
def my_analyses(
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    analyses = (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.created_at.desc())
        .all()
    )
    return {
        "analyses": [
            {
                "id": a.id,
                "linkedin_url": a.linkedin_url,
                "score_before": a.score_before,
                "created_at": a.created_at.isoformat(),
            }
            for a in analyses
        ],
        "total": len(analyses),
    }


@app.post("/api/create-profile")
async def create_profile_route(
    body: CreateProfileRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    result = await create_profile_from_scratch(body.dict())
    return result


@app.post("/api/generate-post")
async def generate_post_route(
    body: GeneratePostRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    """
    Génère 3 versions d'un post LinkedIn optimisé depuis une idée brute.
    - Non connecté : bloqué → doit créer un compte
    - Gratuit       : 3 posts/mois — reset le 1er du mois
    - Candidat/Pro  : illimité
    """
    # Validation idée
    if not body.idee or len(body.idee.strip()) < 5:
        raise HTTPException(
            status_code=422,
            detail="L'idée est trop courte. Décris ton idée en 2-3 phrases minimum."
        )

    # Auth obligatoire
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Connecte-toi pour générer des posts LinkedIn. C'est gratuit ! 🚀"
        )

    # Reset mensuel si nécessaire
    _check_and_reset_posts(current_user, db)

    # Vérification quota (plan free uniquement)
    if current_user.plan == "free":
        remaining = _posts_remaining(current_user)
        if remaining <= 0:
            raise HTTPException(
                status_code=403,
                detail=f"Tu as utilisé tes {FREE_POSTS_LIMIT} posts gratuits ce mois-ci. Passe au plan Candidat pour des posts illimités. 🚀"
            )

    # Génération IA
    result = await generate_linkedin_post(body.dict())

    # Incrémenter le compteur (plan free uniquement)
    if current_user.plan == "free":
        current_user.posts_used = (current_user.posts_used or 0) + 1
        db.commit()
        db.refresh(current_user)

    # Sauvegarder en DB pour l'historique
    post_record = Post(
        user_id=current_user.id,
        idee=body.idee[:200] if body.idee else "",
        ton=body.ton or "tous",
        secteur=body.secteur or "",
        contenu=json.dumps(result.get("posts", [])),
    )
    db.add(post_record)
    db.commit()

    # Quota restant dans la réponse
    result["posts_remaining"] = _posts_remaining(current_user)
    result["posts_used"] = current_user.posts_used or 0
    result["is_unlimited"] = current_user.plan != "free"

    return result


@app.get("/api/my-posts")
def my_posts(
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Retourne l'historique des posts générés par l'utilisateur."""
    posts = (
        db.query(Post)
        .filter(Post.user_id == current_user.id)
        .order_by(Post.created_at.desc())
        .limit(20)
        .all()
    )
    return {
        "posts": [
            {
                "id": p.id,
                "idee": p.idee,
                "ton": p.ton,
                "secteur": p.secteur,
                "contenu": json.loads(p.contenu) if p.contenu else [],
                "created_at": p.created_at.isoformat(),
            }
            for p in posts
        ],
        "total": len(posts),
    }