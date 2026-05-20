import anthropic
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """Tu es Link2Job, un expert en personal branding LinkedIn et en stratégie de recherche d'emploi.
Tu analyses des profils LinkedIn et tu génères des recommandations précises et actionnables.
Tu réponds TOUJOURS en JSON valide, sans aucun texte avant ou après.
Tu es direct, bienveillant, et tu parles en français.
Tu ne mens jamais sur les données — tu travailles avec ce que tu as."""

# ── FILTRE ANTI-IA ── session 14
FILTRE_ANTI_IA = """
MOTS ET EXPRESSIONS STRICTEMENT INTERDITS — ne jamais utiliser, même partiellement :
- plonger, naviguer, façonner, démêler, orchestrer, appréhender
- "il est crucial de", "dans le paysage actuel", "en conclusion"
- "il convient de noter", "à l'ère du numérique", "paradigme"
- "synergies", "holistique", "proactif", "levier stratégique"
- "dans cet article", "n'hésitez pas à", "je suis ravi(e) de partager"
- "force est de constater", "à l'heure où", "incontournable"
- "résilience", "agilité", "écosystème", "disruption", "game-changer"
- "il va sans dire", "au final", "en tant que tel", "dans ce sens"
Ces expressions trahissent immédiatement un texte généré par IA.
Écris comme un humain qui parle vrai — phrases courtes, directes, personnelles.
"""


async def analyze_profile(profile: dict, score_details: dict) -> dict:
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
1. Donner une recommandation concrète et actionable pour chaque section
2. Générer 3 propositions de titres professionnels optimisés
3. Générer un résumé LinkedIn optimisé (About) de 500-800 caractères
4. Donner un conseil stratégique sur la visibilité recruteurs

Réponds UNIQUEMENT avec ce JSON (aucun texte avant/après) :
{{
  "recommendations": {{
    "headline": {{"score": {score_details.get("headline")}, "max": 20, "priority": "haute|moyenne|basse", "conseil": "..."}},
    "about": {{"score": {score_details.get("about")}, "max": 20, "priority": "haute|moyenne|basse", "conseil": "..."}},
    "photo": {{"score": {score_details.get("photo")}, "max": 15, "priority": "haute|moyenne|basse", "conseil": "..."}},
    "experience": {{"score": {score_details.get("experience")}, "max": 15, "priority": "haute|moyenne|basse", "conseil": "..."}},
    "skills": {{"score": {score_details.get("skills")}, "max": 10, "priority": "haute|moyenne|basse", "conseil": "..."}},
    "recommendations": {{"score": {score_details.get("recommendations")}, "max": 5, "priority": "haute|moyenne|basse", "conseil": "..."}},
    "visibility": {{"conseil": "Conseil stratégique sur visibilité recruteurs"}}
  }},
  "optimized_texts": {{
    "headline_suggestions": ["Titre 1", "Titre 2", "Titre 3"],
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
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except json.JSONDecodeError as e:
        print(f"[ai_agent] JSON invalide : {e}")
        return _fallback_response(score_details)
    except Exception as e:
        print(f"[ai_agent] Erreur Claude API : {e}")
        return _fallback_response(score_details)


def _fallback_response(score_details: dict) -> dict:
    return {
        "recommendations": {
            "headline": {"score": score_details.get("headline", 0), "max": 20, "priority": "haute", "conseil": "Optimise ton titre avec ton rôle, ta spécialité et un mot-clé sectoriel."},
            "about": {"score": score_details.get("about", 0), "max": 20, "priority": "haute", "conseil": "Rédige un résumé de 500+ caractères qui raconte ton parcours et ta valeur ajoutée."},
            "photo": {"score": score_details.get("photo", 0), "max": 15, "priority": "haute" if score_details.get("photo", 0) == 0 else "basse", "conseil": "Ajoute une photo professionnelle — fond neutre, sourire, cadrage épaules."},
            "experience": {"score": score_details.get("experience", 0), "max": 15, "priority": "moyenne", "conseil": "Détaille chaque expérience avec des résultats chiffrés."},
            "skills": {"score": score_details.get("skills", 0), "max": 10, "priority": "moyenne", "conseil": "Ajoute au moins 10 compétences pertinentes pour ton secteur."},
            "recommendations": {"score": score_details.get("recommendations", 0), "max": 5, "priority": "basse", "conseil": "Demande une recommandation à un ancien manager ou collègue."},
            "visibility": {"conseil": "Active l'option 'Recruteurs uniquement' plutôt que le badge 'Open to Work' public."}
        },
        "optimized_texts": {
            "headline_suggestions": ["Analyse temporairement indisponible — réessaie dans quelques instants."],
            "about_optimized": "Analyse temporairement indisponible — réessaie dans quelques instants."
        }
    }


async def create_profile_from_scratch(data: dict) -> dict:
    exp_str = ""
    if data.get("experiences"):
        for e in data["experiences"]:
            exp_str += f"\n  - {e.get('poste', '')} chez {e.get('entreprise', 'non précisé')} ({e.get('duree', '')})"
            if e.get("desc"):
                exp_str += f" : {e['desc']}"
    else:
        exp_str = "\n  - Aucune expérience renseignée"

    hard_skills = ", ".join(data.get("hard_skills", [])) or "Non renseigné"
    soft_skills = ", ".join(data.get("soft_skills", [])) or "Non renseigné"

    user_prompt = f"""
Tu dois créer un profil LinkedIn complet et optimisé pour cette personne.

INFORMATIONS PERSONNELLES :
- Prénom : {data.get("prenom", "Non renseigné")}
- Nom : {data.get("nom", "")}
- Secteur : {data.get("secteur", "Non renseigné")}
- Niveau : {data.get("niveau", "Non renseigné")}
- Ville : {data.get("ville", "Non renseignée")}
- Langues : {data.get("langues", "Non renseignées")}

EXPÉRIENCES :{exp_str}

COMPÉTENCES TECHNIQUES (hard skills) : {hard_skills}
QUALITÉS HUMAINES (soft skills) : {soft_skills}

OBJECTIF :
- Type de contrat recherché : {data.get("contrat", "Non précisé")}
- Poste visé : {data.get("poste_vise", "Non précisé")}
- Infos supplémentaires : {data.get("infos_sup", "Aucune")}

Ta mission :
1. Créer 3 titres LinkedIn percutants et optimisés pour les recruteurs
2. Créer un résumé LinkedIn (About) de 600-900 caractères, engageant, en "je"
3. Suggérer 8-12 compétences LinkedIn pertinentes

RÈGLES :
- Utilise le vrai prénom dans le résumé
- Accorde les adjectifs au genre si tu peux le déduire du prénom (sinon reste neutre)
- Le résumé doit se terminer par une invitation à contacter
- Ton : professionnel mais humain, adapté Gen Z
- Réponds UNIQUEMENT en JSON valide, aucun texte avant/après

{{
  "headline_suggestions": ["Titre 1", "Titre 2", "Titre 3"],
  "about_optimized": "Résumé LinkedIn complet ici...",
  "skills_suggested": ["Compétence 1", "Compétence 2"]
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
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except json.JSONDecodeError as e:
        print(f"[ai_agent] create_profile JSON invalide : {e}")
        return _fallback_create_profile(data)
    except Exception as e:
        print(f"[ai_agent] create_profile erreur : {e}")
        return _fallback_create_profile(data)


def _fallback_create_profile(data: dict) -> dict:
    prenom = data.get("prenom", "")
    contrat = data.get("contrat", "poste")
    poste = data.get("poste_vise", data.get("secteur", ""))
    ville = data.get("ville", "France")
    skills = data.get("hard_skills", []) + data.get("soft_skills", [])
    return {
        "headline_suggestions": [
            f"{poste} | {contrat} | {ville} 🚀",
            f"Cherche {contrat} en {poste} · {data.get('secteur', '')}",
            f"🎯 {poste} · Disponible pour un {contrat}"
        ],
        "about_optimized": (
            f"{prenom}, passionné(e) par {data.get('secteur', 'mon domaine')}, "
            f"je recherche un {contrat}{' en tant que ' + poste if poste else ''}.\n\n"
            f"N'hésitez pas à me contacter !"
        ),
        "skills_suggested": skills[:10]
    }


async def generate_linkedin_post(data: dict) -> dict:
    idee = data.get("idee", "")
    secteur = data.get("secteur", "")
    poste = data.get("poste", "")
    ton_demande = data.get("ton", "tous")

    user_prompt = f"""
Tu dois générer 3 posts LinkedIn optimisés pour l'algorithme à partir d'une idée brute.

IDÉE BRUTE DE L'UTILISATEUR :
"{idee}"

CONTEXTE :
- Secteur : {secteur or "Non précisé"}
- Poste visé : {poste or "Non précisé"}
- Ton demandé : {ton_demande}

{FILTRE_ANTI_IA}

RÈGLES ABSOLUES pour chaque post :
1. Hook percutant en PREMIÈRE LIGNE (max 2 lignes) — c'est ce qui s'affiche avant "voir plus"
2. Structure narrative : situation → action → résultat ou enseignement
3. Longueur : 1200-1500 caractères EXACTEMENT (compter espaces inclus)
4. 5 à 8 hashtags pertinents et sectoriels à la fin
5. 1 call-to-action final (question ouverte ou invitation à commenter)
6. Emojis stratégiques : 3-5 max, bien placés, jamais en excès
7. Pas de "Je suis ravi(e) de partager..." — direct et authentique
8. Ton adapté Gen Z : humain, sans jargon corporate inutile

DÉFINITIONS DES TONS :
- "inspirant" : storytelling émotionnel, parcours, leçon de vie, accroche forte
- "expert" : ton crédible, données chiffrées, analyse, valeur ajoutée concrète
- "authentique" : ton humain, accessible, Gen Z friendly, parle vrai

Réponds UNIQUEMENT en JSON valide, aucun texte avant/après :
{{
  "posts": [
    {{
      "ton": "inspirant",
      "contenu": "Post complet ici avec les hashtags intégrés à la fin...",
      "hashtags": ["#hashtag1", "#hashtag2"],
      "chars": 1350,
      "hook": "Première ligne du post"
    }},
    {{
      "ton": "expert",
      "contenu": "Post complet ici avec les hashtags intégrés à la fin...",
      "hashtags": ["#hashtag1", "#hashtag2"],
      "chars": 1280,
      "hook": "Première ligne du post"
    }},
    {{
      "ton": "authentique",
      "contenu": "Post complet ici avec les hashtags intégrés à la fin...",
      "hashtags": ["#hashtag1", "#hashtag2"],
      "chars": 1420,
      "hook": "Première ligne du post"
    }}
  ]
}}
"""
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except json.JSONDecodeError as e:
        print(f"[ai_agent] generate_post JSON invalide : {e}")
        return _fallback_generate_post(data)
    except Exception as e:
        print(f"[ai_agent] generate_post erreur : {e}")
        return _fallback_generate_post(data)


def _fallback_generate_post(data: dict) -> dict:
    idee = data.get("idee", "mon expérience")
    return {
        "posts": [
            {"ton": "inspirant", "contenu": f"💡 {idee}\n\n#LinkedIn #Carrière", "hashtags": ["#LinkedIn"], "chars": 50, "hook": f"💡 {idee}"},
            {"ton": "expert", "contenu": f"📊 {idee}\n\n#Expertise", "hashtags": ["#Expertise"], "chars": 40, "hook": f"📊 {idee}"},
            {"ton": "authentique", "contenu": f"Soyons honnêtes : {idee}\n\n#Authenticité", "hashtags": ["#Authenticité"], "chars": 50, "hook": f"Soyons honnêtes : {idee}"}
        ]
    }


# ── ✅ NOUVEAU : analyze_profile_from_pdf avec données activité ──
def analyze_profile_from_pdf(pdf_text: str, activity_data: dict = None) -> dict:
    """
    Analyse un profil LinkedIn extrait d'un PDF.
    activity_data (optionnel) :
      - posts_count : int   → posts publiés ce mois
      - comments_regularly : bool → commente régulièrement
      - creator_mode : bool → mode créateur activé
    """

    # ── Contexte activité ──
    if activity_data:
        posts = activity_data.get("posts_count", 0)
        comments = activity_data.get("comments_regularly", False)
        creator = activity_data.get("creator_mode", False)

        # Score logique
        if posts >= 4 and comments:
            activity_score_hint = "score élevé (4-5/5)"
        elif posts >= 2 or comments:
            activity_score_hint = "score moyen (2-3/5)"
        else:
            activity_score_hint = "score bas (0-1/5)"

        activity_context = f"""
DONNÉES D'ACTIVITÉ RENSEIGNÉES PAR L'UTILISATEUR :
- Posts publiés ce mois : {posts}
- Commente régulièrement dans son secteur : {"Oui" if comments else "Non"}
- Mode créateur LinkedIn activé : {"Oui" if creator else "Non"}
→ Sur cette base, donne un {activity_score_hint} pour la section "activity".
→ Dans le conseil activité, sois précis : dis exactement quoi faire pour progresser
   (ex: publier X posts/semaine, commenter Y posts/jour, activer le mode créateur, etc.)
"""
    else:
        activity_context = """
ATTENTION : L'utilisateur n'a pas renseigné son activité LinkedIn.
Le PDF LinkedIn n'exporte pas les posts ni les interactions — ne pas pénaliser injustement.
→ Donne 2/5 par défaut avec ce conseil précis :
  "Le PDF ne capture pas ton activité réelle. Pour améliorer ce score :
   publie au moins 2 posts/semaine dans ton secteur, commente 3 posts/jour,
   et active le mode créateur LinkedIn dans les paramètres de ton profil."
"""

    prompt = f"""Tu es un expert LinkedIn et recruteur senior avec 15 ans d'expérience.
Voici le contenu extrait d'un profil LinkedIn exporté en PDF :

---
{pdf_text[:6000]}
---

{activity_context}

Analyse ce profil et retourne UNIQUEMENT un JSON valide avec cette structure exacte.
Pour CHAQUE section, le conseil doit être ACTIONNABLE et PRÉCIS — pas générique.
Dis exactement QUOI faire, COMMENT, et si possible en COMBIEN DE TEMPS.

{{
  "score_before": <entier 0-100>,
  "score_details": {{
    "headline": <0-20>,
    "about": <0-20>,
    "photo": <0-15>,
    "experience": <0-15>,
    "skills": <0-10>,
    "education": <0-10>,
    "recommendations": <0-5>,
    "activity": <0-5>
  }},
  "recommendations": {{
    "headline": {{"score": <int>, "priority": "haute|moyenne|basse", "conseil": "<conseil précis et actionnable>"}},
    "about": {{"score": <int>, "priority": "haute|moyenne|basse", "conseil": "<conseil précis et actionnable>"}},
    "photo": {{"score": <int>, "priority": "haute|moyenne|basse", "conseil": "<conseil précis et actionnable>"}},
    "experience": {{"score": <int>, "priority": "haute|moyenne|basse", "conseil": "<conseil précis et actionnable>"}},
    "skills": {{"score": <int>, "priority": "haute|moyenne|basse", "conseil": "<conseil précis et actionnable>"}},
    "education": {{"score": <int>, "priority": "haute|moyenne|basse", "conseil": "<conseil précis et actionnable>"}},
    "recommendations": {{"score": <int>, "priority": "haute|moyenne|basse", "conseil": "<conseil précis et actionnable>"}},
    "activity": {{"score": <int>, "priority": "haute|moyenne|basse", "conseil": "<conseil précis et actionnable>"}}
  }},
  "optimized_texts": {{
    "headline_suggestions": ["<titre 1>", "<titre 2>", "<titre 3>"],
    "about_optimized": "<résumé LinkedIn optimisé 3-5 lignes, accrocheur, avec mots-clés>"
  }}
}}

Règles :
- Base-toi sur le contenu du PDF + les données d'activité fournies
- Si une section est absente, score bas + conseil pour la remplir
- Titres et résumé en français
- Aucun markdown, aucune explication, juste le JSON"""

    client_local = anthropic.Anthropic()
    message = client_local.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = message.content[0].text.strip()
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        raw = match.group()
    return json.loads(raw)