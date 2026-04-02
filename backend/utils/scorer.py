"""
scorer.py — Calcule le score LinkedIn 0-100 par section.

Pondération :
  Titre professionnel   20 pts
  Résumé (About)        20 pts
  Photo de profil       15 pts
  Expériences           15 pts
  Compétences           10 pts
  Formation             10 pts
  Recommandations        5 pts
  Activité               5 pts
  ─────────────────────────────
  TOTAL                100 pts
"""


def compute_score(profile: dict) -> dict:
    scores = {}

    # ── Titre professionnel (20 pts) ──────────────────────
    headline = profile.get("headline", "")
    scores["headline"] = _score_headline(headline)

    # ── Résumé / About (20 pts) ───────────────────────────
    about = profile.get("about", "")
    scores["about"] = _score_about(about)

    # ── Photo de profil (15 pts) ──────────────────────────
    scores["photo"] = 15 if profile.get("has_photo") else 0

    # ── Expériences (15 pts) ─────────────────────────────
    experiences = profile.get("experiences", [])
    scores["experience"] = _score_experience(experiences)

    # ── Compétences (10 pts) ─────────────────────────────
    skills = profile.get("skills", [])
    scores["skills"] = _score_skills(skills)

    # ── Formation (10 pts) ────────────────────────────────
    education = profile.get("education", [])
    scores["education"] = 10 if len(education) > 0 else 0

    # ── Recommandations (5 pts) ───────────────────────────
    reco_count = profile.get("recommendations_count", 0)
    scores["recommendations"] = _score_recommendations(reco_count)

    # ── Activité (5 pts) ──────────────────────────────────
    scores["activity"] = 5 if profile.get("has_activity") else 0

    # ── Total ─────────────────────────────────────────────
    total = sum(scores.values())
    scores["total"] = min(total, 100)  # Plafond à 100

    return scores


# ── HELPERS ─────────────────────────────────────────────

def _score_headline(headline: str) -> int:
    """
    0  = vide
    5  = générique ("Étudiant", "En recherche d'emploi")
    10 = présent mais peu optimisé
    15 = bon (contient un rôle + contexte)
    20 = excellent (rôle + mots-clés + secteur ou valeur ajoutée)
    """
    if not headline:
        return 0

    words = headline.split()
    if len(words) <= 2:
        return 5

    # Mots-clés génériques négatifs
    generic = {"étudiant", "student", "en recherche", "open to work", "job seeker", "candidat"}
    low = headline.lower()
    if any(g in low for g in generic):
        return 8

    # Bon si contient un séparateur (|, ·, —) = structure professionnelle
    has_separator = any(c in headline for c in ["|", "·", "—", "-"])
    if has_separator and len(words) >= 5:
        return 20
    if len(words) >= 4:
        return 15

    return 10


def _score_about(about: str) -> int:
    """
    0  = vide
    5  = très court (< 50 chars)
    10 = présent mais court (< 200 chars)
    15 = bon (200-500 chars)
    20 = excellent (> 500 chars avec substance)
    """
    if not about:
        return 0
    n = len(about)
    if n < 50:
        return 5
    if n < 200:
        return 10
    if n < 500:
        return 15
    return 20


def _score_experience(experiences: list) -> int:
    """
    0  = aucune expérience
    5  = 1 expérience
    10 = 2 expériences
    15 = 3+ expériences
    """
    n = len(experiences)
    if n == 0:
        return 0
    if n == 1:
        return 5
    if n == 2:
        return 10
    return 15


def _score_skills(skills: list) -> int:
    """
    0  = aucune compétence
    4  = 1-4 compétences
    7  = 5-9 compétences
    10 = 10+ compétences
    """
    n = len(skills)
    if n == 0:
        return 0
    if n < 5:
        return 4
    if n < 10:
        return 7
    return 10


def _score_recommendations(count: int) -> int:
    if count == 0:
        return 0
    if count == 1:
        return 2
    if count >= 3:
        return 5
    return 3