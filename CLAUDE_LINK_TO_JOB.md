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
- stripe_router.py créé avec create-checkout + webhook + subscription-status
- Bouton "Commencer — 9,99€/mois" connecté à upgradeToCandidat()

### Session 3 — 3 Avril 2026
- ✅ Bug Stripe UnicodeEncodeError corrigé (caractère ← dans les données)
- ✅ Flow paiement Stripe end-to-end fonctionnel en test
- ✅ Stripe CLI installé sur Windows (stripe version 1.40.0)
- ✅ Webhook Stripe forwarding via `stripe listen --forward-to localhost:8000/api/stripe/webhook`
- ✅ Bug stripe_router.py corrigé : session_data.get() → notation attribut Stripe
- ✅ Plan mis à jour en DB après paiement (plan: "candidat")
- ✅ Nav affiche "∞ Illimité" en vert pour les abonnés Candidat
- ✅ Dashboard affiche "Plan Candidat — illimité ✅" après upgrade
- ✅ initAuth(forceRefresh) dans index.html : un seul fetch /api/auth/me au démarrage
- ✅ dashboard.html : fetch /api/auth/me au retour Stripe + update localStorage
- ✅ Plus de race condition entre les fetch concurrents

### Commits GitHub
- e9398b2 — initial project structure
- 58637c1 — MVP V1 fonctionnel
- 381fb4c — frontend connecté au backend
- 50b67cc — guide visibilité recruteurs + CLAUDE.md session 1
- ddaceab — auth modal complet
- 8d787da — dashboard progression (dernier commit pushé)
- ⚠️ Session 3 non encore commitée — à pusher !

---

## 🏗️ Architecture technique

```
backend/
├── main.py              ← FastAPI
├── auth.py              ← Register/login/me + JWT + argon2
├── database.py          ← SQLAlchemy — User + Analysis models
├── stripe_router.py     ← Stripe checkout + webhook + status (CORRIGÉ session 3)
├── .env                 ← Toutes les clés (jamais commiter)
├── .env.example
├── requirements.txt
└── utils/
    ├── __init__.py
    ├── linkedin_parser.py  ← MOCK actif en dev
    ├── scorer.py
    └── ai_agent.py

frontend/
├── index.html        ← Landing + formulaire + résultats + modal auth + Stripe
└── dashboard.html    ← Dashboard progression SVG + historique
```

### Endpoints backend actifs
```
GET  /api/health
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
POST /api/analyze-profile
GET  /api/my-analyses
POST /api/stripe/create-checkout   ← CORRIGÉ session 3
POST /api/stripe/webhook           ← CORRIGÉ session 3 (notation attribut Stripe)
GET  /api/stripe/subscription-status
```

### Variables .env nécessaires
```
ANTHROPIC_API_KEY=sk-ant-...
SECRET_KEY=L2J#xK9mP2qL8nR4vT6wY1uI3oE5aS7d
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PRICE_ID=price_1...
STRIPE_WEBHOOK_SECRET=whsec_...    ← OBLIGATOIRE (Stripe CLI en dev, dashboard Stripe en prod)
```

### ⚠️ Setup dev obligatoire (3 terminaux)
```powershell
# Terminal 1 — Backend
cd C:\Projects\link_to_job\backend
python -m uvicorn main:app --reload

# Terminal 2 — Frontend
cd C:\Projects\link_to_job\frontend
python -m http.server 5500

# Terminal 3 — Stripe CLI (NOUVEAU — obligatoire pour les webhooks)
stripe listen --forward-to localhost:8000/api/stripe/webhook
```

→ Backend Swagger : http://127.0.0.1:8000/docs
→ Frontend : http://localhost:5500/index.html
→ Dashboard : http://localhost:5500/dashboard.html

**⚠️ Toujours utiliser localhost:5500 et jamais file:// pour le frontend**
**⚠️ Le terminal Stripe CLI doit tourner pour que les webhooks fonctionnent en dev**

---

## 🎨 Charte graphique

```
Primaire :       #FF6B00 (orange vif)
Primaire foncé : #D95A00
Fond sombre :    #0C0C18 / #1A1A2E
Succès :         #22C55E
Erreur :         #EF4444
Accent bleu :    #0A66C2 (LinkedIn)
Typo titres :    Syne 800
Typo corps :     DM Sans
Border radius :  sm=8px md=14px lg=22px xl=32px
```

---

## 🗺️ Feuille de route

### V1 — "Le Profil Parfait" ← ON EST ICI
- [x] Landing page complète
- [x] Analyse IA Claude Sonnet — score + recommandations + textes
- [x] Guide interactif "Visibilité recruteurs"
- [x] Auth register/login JWT + compteur 3 analyses gratuites
- [x] Dashboard progression SVG + historique
- [x] Stripe checkout + webhook fonctionnel end-to-end ✅
- [x] Nav "∞ Illimité" pour les abonnés ✅
- [ ] Formulaire saisie guidée (remplace mock LinkedIn)
- [ ] Export rapport PDF
- [ ] Déploiement Railway (prod)

### V2 — "La Candidature Intelligente"
- [ ] Extension Chrome Manifest V3
- [ ] CV uploadé → moteur ATS cv-ats-ready
- [ ] Lettre de motivation IA contextuelle
- [ ] Dashboard suivi candidatures

### V3 — "L'Écosystème Emploi"
- [ ] Volet Employeur
- [ ] Multi-plateformes (Indeed, WTTJ, France Travail)
- [ ] Licences B2B grandes écoles
- [ ] App mobile

---

## 💰 Modèle économique & pitch

### Plans
| Plan | Prix | Inclus |
|------|------|--------|
| Gratuit | 0€ | 3 analyses (cycle amélioration) |
| Candidat | 9,99€/mois | Analyses illimitées + textes IA |
| Candidat Pro | 19,99€/mois | + Extension Chrome + suivi |
| Grande École | 500-2000€/an | Licence B2B |
| Employeur | 99-299€/mois | Tableau de bord V3 |

### Arguments pitch 9,99€
```
Coût par abonné/mois :
  Claude Sonnet (10 analyses)  ≈ 0,30€
  Hébergement Railway          ≈ 0,05€
  Stripe commission            ≈ 0,35€
  ─────────────────────────────────────
  Total coût                   ≈ 0,70€
  Marge nette                  ≈ 9,29€ (93%)

Projections MRR :
  10 abonnés  →   100€/mois →  93€ marge
  100 abonnés → 1 000€/mois → 930€ marge
  500 abonnés → 5 000€/mois → 4 650€ marge

Psychologie prix :
  - Moins de 10€ → pas besoin autorisation parentale
  - ROI si job à 2000€/mois → rentabilisé en 1h de travail
  - Référence : Spotify 9,99€ → premium mais accessible
  - 93% de marge → impossible de perdre de l'argent
  - Ne jamais baisser le prix affiché
```

---

## 🧠 Décisions produit importantes

- **LinkedIn parser = MOCK** → formulaire saisie guidée (100% légal, gratuit)
- **Proxycurl fermé** (lawsuit LinkedIn 2025). Netrows = liste d'attente.
- **3 analyses gratuites** = même profil, cycle amélioration
- **Dashboard = produit payant** — progression dans le temps justifie l'abo
- **Churn mitigation** = dashboard progression (mécanisme Duolingo)
- **CV + LM** = feature V2, moteur cv-ats-ready réutilisé
- **Stripe CLI** = obligatoire en dev pour les webhooks (whsec_ de dev ≠ prod)
- **En prod** : remplacer whsec_ dev par le vrai secret du dashboard Stripe live
