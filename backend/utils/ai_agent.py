import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """Tu es Link2Job, un expert en personal branding LinkedIn et en stratégie de recherche d'emploi.
Tu analyses des profils LinkedIn et tu génères des recommandations précises et actionnables.
Tu réponds TOUJOURS en JSON valide, sans aucun texte avant ou après.
Tu es direct, bienveillant, et tu parles en français.
Tu ne mens jamais sur les données — tu travailles avec ce que tu as."""


async def analyze_profile(profile: dict, score_details: dict) -> dict:
    """
    Envoie le profil + les scores à Claude Sonnet.
    Retourne des recommandations et des textes optimisés.
    """

    user_prompt = f"""
Voici le profil LinkedIn d'un candidat à analyser :

DONNÉES DU PROFIL :
- Nom : {profile.get("name", "Non renseigné")}
- Titre actuel : {profile.get("headline", "Vide")}
- Résumé (About) : {profile.get("about", "Vide")}
- Localisation : {profile.get("location", "Non renseignée")}
- Expériences : {len(profile.get("experiences", []))} entrée(s)
- Compétences : {len(profile.get("skills", []))} compétence(s) : {", ".join(profile.get("skills", [])[:10])}
- Formation : {len(profile.get("education", []))} entrée(s)
- Recommandations : {profile.get("recommendations_count", 0)}
- Photo de profil : {"Oui" if profile.get("has_photo") else "Non"}
- Activité récente : {"Oui" if profile.get("has_activity") else "Non"}

SCORES PAR SECTION (sur les points max) :
- Titre : {score_details.get("headline")}/20
- Résumé : {score_details.get("about")}/20
- Photo : {score_details.get("photo")}/15
- Expériences : {score_details.get("experience")}/15
- Compétences : {score_details.get("skills")}/10
- Formation : {score_details.get("education")}/10
- Recommandations : {score_details.get("recommendations")}/5
- Activité : {score_details.get("activity")}/5
- SCORE TOTAL : {score_details.get("total")}/100

Ta mission :
1. Donner une recommandation concrète et actioable pour chaque section (priorité : les plus faibles d'abord)
2. Générer 3 propositions de titres professionnels optimisés
3. Générer un résumé LinkedIn optimisé (About) de 500-800 caractères
4. Donner un conseil stratégique sur la visibilité recruteurs (évite "Open to Work" public — conseille "Recruteurs uniquement")

Réponds UNIQUEMENT avec ce JSON (aucun texte avant/après) :
{{
  "recommendations": {{
    "headline": {{
      "score": {score_details.get("headline")},
      "max": 20,
      "priority": "haute|moyenne|basse",
      "conseil": "..."
    }},
    "about": {{
      "score": {score_details.get("about")},
      "max": 20,
      "priority": "haute|moyenne|basse",
      "conseil": "..."
    }},
    "photo": {{
      "score": {score_details.get("photo")},
      "max": 15,
      "priority": "haute|moyenne|basse",
      "conseil": "..."
    }},
    "experience": {{
      "score": {score_details.get("experience")},
      "max": 15,
      "priority": "haute|moyenne|basse",
      "conseil": "..."
    }},
    "skills": {{
      "score": {score_details.get("skills")},
      "max": 10,
      "priority": "haute|moyenne|basse",
      "conseil": "..."
    }},
    "recommendations": {{
      "score": {score_details.get("recommendations")},
      "max": 5,
      "priority": "haute|moyenne|basse",
      "conseil": "..."
    }},
    "visibility": {{
      "conseil": "Conseil stratégique sur visibilité recruteurs"
    }}
  }},
  "optimized_texts": {{
    "headline_suggestions": [
      "Titre suggestion 1",
      "Titre suggestion 2",
      "Titre suggestion 3"
    ],
    "about_optimized": "Résumé LinkedIn optimisé complet ici..."
  }}
}}
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw = message.content[0].text.strip()

        # Nettoyage au cas où le modèle ajoute des backticks
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        return result

    except json.JSONDecodeError as e:
        print(f"[ai_agent] JSON invalide : {e}")
        return _fallback_response(score_details)

    except Exception as e:
        print(f"[ai_agent] Erreur Claude API : {e}")
        return _fallback_response(score_details)


def _fallback_response(score_details: dict) -> dict:
    """Réponse de secours si l'API échoue."""
    return {
        "recommendations": {
            "headline": {
                "score": score_details.get("headline", 0),
                "max": 20,
                "priority": "haute",
                "conseil": "Optimise ton titre avec ton rôle, ta spécialité et un mot-clé sectoriel."
            },
            "about": {
                "score": score_details.get("about", 0),
                "max": 20,
                "priority": "haute",
                "conseil": "Rédige un résumé de 500+ caractères qui raconte ton parcours et ta valeur ajoutée."
            },
            "photo": {
                "score": score_details.get("photo", 0),
                "max": 15,
                "priority": "haute" if score_details.get("photo", 0) == 0 else "basse",
                "conseil": "Ajoute une photo professionnelle — fond neutre, sourire, cadrage épaules."
            },
            "experience": {
                "score": score_details.get("experience", 0),
                "max": 15,
                "priority": "moyenne",
                "conseil": "Détaille chaque expérience avec des résultats chiffrés."
            },
            "skills": {
                "score": score_details.get("skills", 0),
                "max": 10,
                "priority": "moyenne",
                "conseil": "Ajoute au moins 10 compétences pertinentes pour ton secteur."
            },
            "recommendations": {
                "score": score_details.get("recommendations", 0),
                "max": 5,
                "priority": "basse",
                "conseil": "Demande une recommandation à un ancien manager ou collègue."
            },
            "visibility": {
                "conseil": "Active l'option 'Recruteurs uniquement' plutôt que le badge 'Open to Work' public."
            }
        },
        "optimized_texts": {
            "headline_suggestions": [
                "Analyse temporairement indisponible — réessaie dans quelques instants.",
            ],
            "about_optimized": "Analyse temporairement indisponible — réessaie dans quelques instants."
        }
    }