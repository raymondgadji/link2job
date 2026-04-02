from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from utils.linkedin_parser import parse_linkedin_profile
from utils.ai_agent import analyze_profile
from utils.scorer import compute_score

app = FastAPI(title="Link2Job API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod : remplace par ton domaine
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── MODELS ──────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    linkedin_url: str  # ex: https://www.linkedin.com/in/raymond-gadji

class AnalyzeResponse(BaseModel):
    score_before: int
    score_details: dict
    recommendations: dict
    optimized_texts: dict

# ── ROUTES ──────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.1.0"}


@app.post("/api/analyze-profile", response_model=AnalyzeResponse)
async def analyze_profile_route(body: AnalyzeRequest):
    # 1. Parse le profil LinkedIn public
    profile_data = await parse_linkedin_profile(body.linkedin_url)
    if not profile_data:
        raise HTTPException(status_code=422, detail="Profil LinkedIn introuvable ou non public.")

    # 2. Calcule le score brut par section
    score_details = compute_score(profile_data)

    # 3. Analyse IA + génération de textes optimisés
    ai_result = await analyze_profile(profile_data, score_details)

    return AnalyzeResponse(
        score_before=score_details["total"],
        score_details=score_details,
        recommendations=ai_result["recommendations"],
        optimized_texts=ai_result["optimized_texts"],
    )