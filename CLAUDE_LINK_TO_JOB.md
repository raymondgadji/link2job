# CLAUDE.md — LINK TO JOB
> Mémoire projet complète. À coller en début de chaque nouvelle session.
> Objectif : N°1 européen de la recherche d'emploi et de stage automatisée par IA.

---

## 🎯 Vision produit

**LINK TO JOB** — L'app qui trouve ton emploi pendant que tu dors.
**Tagline** : "Tu te connectes une fois. On s'occupe de ta carrière."
**URL cible** : linktojob.fr (à acheter)
**Rôles** : Founder (Raymond) + CTO (Claude)
**Repo GitHub** : https://github.com/raymondgadji/link2job

### Branding
- **Logo / UI compacte** : Link2Job (tout collé, le 2 en orange)
- **Nom complet / communication** : LINK TO JOB
- Les deux coexistent selon le contexte

### Mission
Démocratiser l'accès à l'emploi pour tous — du lycéen de 16 ans qui cherche son premier stage jusqu'au cadre en reconversion — grâce à l'automatisation intelligente et éthique de la recherche d'emploi sur LinkedIn, puis sur tous les réseaux.

---

## 👤 Profil Founder
- Raymond GADJI — gadjiraymond7@gmail.com
- Passionné IA, data science, entrepreneuriat
- Bootcamp data analyse + certification Hugging Face (smol agents)
- Stack : HTML/CSS/JS (intermédiaire), Python (débutant)
- Projets : Trajets Verts Paris · IA Éléphants de Côte d'Ivoire · cv-ats-ready.fr
- Réseau : EmLyon Paris (formation Développeur)
- Objectif : Station F / French Tech → N°1 européen

---

## ✅ CE QUI A ÉTÉ BUILDÉ

### Session 1 — 2 Avril 2026
- Landing page complète (hero, stats, how it works, features, pricing, FAQ, footer)
- Formulaire analyse LinkedIn dans le hero avec loading animé 4 étapes
- Section résultats : score ring SVG animé 0-100, mini-barres par section
- Recommandations IA par section avec priorité haute/moyenne/basse
- 3 titres LinkedIn optimisés générés par Claude Sonnet + bouton Copier
- Résumé About complet généré par IA + bouton Copier
- Guide interactif "Visibilité recruteurs" (5 étapes, simulation UI LinkedIn)
- Backend FastAPI : /api/health + /api/analyze-profile
- Scorer LinkedIn 0-100 pondéré par section (8 critères)
- AI agent Claude Sonnet avec prompt FR + fallback propre
- LinkedIn parser httpx + BeautifulSoup (mock dev actif)

### Session 2 — 3 Avril 2026
- Auth modal register/login connecté au frontend (JWT localStorage)
- Token JWT envoyé à chaque appel API (Authorization Bearer)
- Quota freemium affiché en temps réel dans la nav ("X analyses restantes")
- Barre quota dans les résultats avec warning si ≤ 1 restante
- Flow intelligent : analyse en attente si non connecté → modal → analyse auto
- Backend auth complet : register/login/me + compteur analyses + historique DB
- SQLite en dev (PostgreSQL Railway en prod)
- Dashboard progression : graphique SVG courbe + 4 stats cards + historique
- Lien "📊 Mon dashboard" dans la nav après connexion

### Commits GitHub
- e9398b2 — initial project structure
- 58637c1 — MVP V1 fonctionnel
- 381fb4c — frontend connecté au backend
- 50b67cc — guide visibilité recruteurs + CLAUDE.md session 1
- ddaceab — auth modal complet
- 8d787da — dashboard progression (dernier commit)

---

## 🏗️ Architecture technique

```
backend/
├── main.py           ← FastAPI v0.2.0 — tous les endpoints
├── auth.py           ← Register/login/me + JWT + compteur freemium
├── database.py       ← SQLAlchemy — User + Analysis models
├── .env              ← ANTHROPIC_API_KEY + SECRET_KEY (jamais commiter)
├── .env.example      ← Template
├── requirements.txt
└── utils/
    ├── __init__.py
    ├── linkedin_parser.py  ← MOCK actif en dev
    ├── scorer.py           ← Score 0-100 (8 sections pondérées)
    └── ai_agent.py         ← Claude Sonnet — analyse + génération

frontend/
├── index.html        ← Landing page + formulaire + résultats + modal auth
└── dashboard.html    ← Dashboard progression SVG + historique
```

### Endpoints backend actifs
```
GET  /api/health
POST /api/auth/register     ← email + password + full_name → JWT
POST /api/auth/login        ← form-data username/password → JWT
GET  /api/auth/me           ← profil user connecté
POST /api/analyze-profile   ← URL LinkedIn → score + recommandations + textes
GET  /api/my-analyses       ← historique analyses de l'user connecté
```

### Stack technique validée
| Couche | Techno |
|--------|--------|
| Frontend | HTML/CSS/JS vanilla |
| Backend | Python FastAPI |
| IA | Claude Sonnet 4 (Anthropic API) |
| Auth | JWT (python-jose) + argon2 (hash passwords) |
| DB Dev | SQLite (fichier local link2job.db) |
| DB Prod | PostgreSQL sur Railway |
| Paiement | Stripe (à intégrer) |

---

## 🎨 Charte graphique

```
Primaire :       #FF6B00 (orange vif)
Primaire foncé : #D95A00
Fond sombre :    #0C0C18 / #1A1A2E
Fond clair :     #FAFAF8
Succès :         #22C55E
Erreur :         #EF4444
Accent bleu :    #0A66C2 (LinkedIn)

Typo titres :    Syne 800
Typo corps :     DM Sans
Border radius :  sm=8px md=14px lg=22px xl=32px
Effets :         Glassmorphism, orbs animés, noise texture, gradients orange
```

---

## 🗺️ Feuille de route

### V1 — "Le Profil Parfait" ← ON EST ICI
- [x] Landing page complète
- [x] Analyse IA (Claude Sonnet) — score + recommandations + textes
- [x] Guide interactif "Visibilité recruteurs"
- [x] Système auth — inscription/connexion JWT + compteur 3 analyses gratuites
- [x] Dashboard progression — graphique SVG + historique
- [ ] **Stripe** — abonnement 9,99€/mois (PROCHAINE ÉTAPE)
- [ ] Formulaire saisie guidée (remplace le mock LinkedIn)
- [ ] Export rapport PDF

### V2 — "La Candidature Intelligente"
- [ ] Extension Chrome Manifest V3
- [ ] Candidature 1 clic avec accord utilisateur
- [ ] CV uploadé → moteur ATS cv-ats-ready (Raymond partagera les fichiers)
- [ ] Lettre de motivation générée par IA + question "Tu veux ajouter quelque chose ?"
- [ ] Dashboard suivi candidatures + relance intelligente

### V3 — "L'Écosystème Emploi"
- [ ] Volet Employeur
- [ ] Indeed, Welcome to the Jungle, France Travail
- [ ] Licences B2B grandes écoles (500-2000€/an)
- [ ] App mobile iOS/Android

---

## 💰 Modèle économique & justification prix (PITCH DECK)

### Plans tarifaires
| Plan | Prix | Inclus |
|------|------|--------|
| Gratuit | 0€ | 3 analyses (cycle amélioration) |
| Candidat | 9,99€/mois | Analyses illimitées + textes IA |
| Candidat Pro | 19,99€/mois | + Extension Chrome + suivi candidatures |
| Grande École | 500-2000€/an | Licence multi-utilisateurs B2B |
| Employeur | 99-299€/mois | Accès profils + tableau de bord (V3) |

### 💡 Justification 9,99€ — Arguments de pitch

**Structure de coûts par abonné (9,99€/mois) :**
```
Claude Sonnet (10 analyses/mois)  ≈ 0,30€
Hébergement Railway               ≈ 0,05€ (mutualisé)
Stripe commission                 ≈ 0,35€
─────────────────────────────────────────
Coût total par abonné             ≈ 0,70€
Marge nette par abonné            ≈ 9,29€
Taux de marge                     ≈ 93%
```

**Projections MRR :**
```
10 abonnés   →   100€/mois  →  93€ marge nette
50 abonnés   →   500€/mois  → 465€ marge nette
100 abonnés  → 1 000€/mois  → 930€ marge nette
500 abonnés  → 5 000€/mois  → 4 650€ marge nette
```

**Pourquoi 9,99€ est le prix parfait :**
- Moins de 10€ → pas besoin d'autorisation parentale (cible lycéens)
- "Moins cher qu'un kebab par semaine" pour un étudiant
- Si ça trouve un job à 2 000€/mois → ROI en 1h de travail
- Référence marché : Netflix 5,99€, Spotify 9,99€ → premium mais accessible
- 93% de marge → on ne peut pas perdre d'argent par abonné

**Le vrai risque = le churn, pas le prix :**
Les utilisateurs trouvent un job et se désabonnent. La réponse :
le dashboard de progression crée de l'attachement (mécanisme Duolingo).
L'utilisateur veut voir son score monter → il reste abonné même après avoir trouvé.

**Règle de pricing :** Ne jamais baisser le prix affiché — ça dévalue le produit.
Promotions ponctuelles OK. Prix catalogue = 9,99€ toujours.

---

## 🧠 Décisions produit importantes

- **"Open to Work" public = déconseillé** — on conseille "Recruteurs uniquement" partout
- **LinkedIn parser = MOCK** — LinkedIn bloque le scraping. Alternative : formulaire de saisie guidée (l'user remplit ses propres données — 100% légal, gratuit, plus précis)
- **Proxycurl est mort** — LinkedIn lawsuit juillet 2025. Netrows = liste d'attente. On reste sur le mock + formulaire guidé.
- **3 analyses gratuites** = 3 analyses du MÊME profil (cycle : analyser → appliquer → re-analyser). Pas 3 URLs différentes.
- **Création profil LinkedIn de zéro** = feature V1 différenciante pour lycéens 16 ans
- **CV + Lettre de motivation** = feature V2, moteur cv-ats-ready réutilisé
- **Dashboard = produit payant** — voir son score évoluer dans le temps justifie l'abonnement

---

## ⚠️ Risques et mitigation

### LinkedIn CGU (CRITIQUE)
V1 : formulaire saisie guidée (données de l'user lui-même → 100% légal)
V2 : extension Chrome simule actions humaines (standard industrie)

### Churn
Mécanisme de rétention : dashboard progression + streak score (comme Duolingo)

### Dépendance Claude API
Fallback propre codé dans ai_agent.py si API down

---

## 🛠️ Pour démarrer une session

```powershell
cd C:\Projects\link_to_job\backend
python -m uvicorn main:app --reload
```
→ Swagger : http://127.0.0.1:8000/docs
→ Frontend : ouvrir frontend/index.html dans Chrome

**Variables .env nécessaires :**
```
ANTHROPIC_API_KEY=sk-ant-...
SECRET_KEY=link2job-dev-secret-change-in-prod
STRIPE_SECRET_KEY=sk_test_...        (à ajouter)
STRIPE_WEBHOOK_SECRET=whsec_...      (à ajouter)
STRIPE_PRICE_ID=price_...            (à ajouter)
```
