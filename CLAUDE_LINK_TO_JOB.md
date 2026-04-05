# CLAUDE.md — LINK TO JOB
> Mémoire projet complète. À coller en début de chaque nouvelle session.
> Objectif : N°1 européen de la recherche d'emploi et de stage automatisée par IA.

---

## 🎯 Vision produit

**LINK TO JOB** — L'app qui trouve ton emploi pendant que tu dors.
**Tagline** : "Le recruteur t'a vu hier, il t'a zappé. Tu veux qu'on règle ça ?"
**URL cible** : link2job.fr ✅ (acheté chez Ionos)
**Backend prod** : https://link2job-production.up.railway.app ✅
**Rôles** : Founder (Raymond) + CTO (Claude)
**Repo GitHub** : https://github.com/raymondgadji/link2job

### Branding
- **Logo / UI compacte** : Link2Job (tout collé, le 2 en orange)
- **Nom complet / communication** : LINK TO JOB
- Les deux coexistent selon le contexte
- **"zappé"** s'affiche en orange dans le hero h1

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

## 💡 IDÉES PRODUIT À IMPLÉMENTER

### 📱 Vision Gen Z / Mobile First
UX mobile à améliorer sur ce qu'on a déjà :
- **Bouton plein écran** "Analyser mon profil →" qui ouvre un bottom sheet natif sur mobile
- **Micro-animations** sur les stats (compteurs animés, pulse sur les chiffres clés)
- **Mode "scan rapide"** avec swipe entre les recommandations comme des stories Instagram
- Le formulaire hero sur mobile est correct mais pas optimal — à retravailler

### ✍️ Générateur de Posts LinkedIn ← FEATURE V2 PRIORITAIRE

**Insight fondateur (même logique que cv-ats-ready.fr) :**
Raymond a créé cv-ats-ready.fr parce qu'il allait sur les LLM pour réécrire son CV et générer des lettres de motivation — il a automatisé ce processus fastidieux. Même constat ici : les professionnels LinkedIn vont sur ChatGPT, copient leur idée, récupèrent un post générique, le retravaillent... C'est laborieux et le résultat est souvent fade.

**Le marché :**
- Des milliers de personnes sur LinkedIn vont sur des LLM pour générer leurs posts
- Ils doivent prompter, copier-coller, reformuler — c'est une friction énorme
- Les novices LinkedIn (Gen Z en recherche d'emploi) veulent se personal brander mais ne savent pas écrire "pro"
- Personne ne leur propose un outil dédié, simple, sans prompt à écrire

**La solution Link2Job :**
Un espace dédié où l'utilisateur écrit juste son idée en 2-3 lignes (langage naturel, pas de prompt), et l'IA génère automatiquement 3 versions du post optimisé LinkedIn :
- **Version Inspirante** — ton storytelling émotionnel, accroche forte
- **Version Expert** — ton crédible, chiffres, valeur ajoutée
- **Version Authentique** — ton humain et accessible, Gen Z friendly

**Ce que l'IA optimise automatiquement :**
- Hook (première ligne = 80% du reach LinkedIn)
- Structure narrative (situation → action → résultat)
- Hashtags pertinents (5-8 max, sectoriels)
- Longueur optimale (1300-1500 caractères pour l'algo LinkedIn)
- Call-to-action final
- Emojis stratégiques (pas trop, pas trop peu)

**Flow utilisateur imaginé :**
```
1. L'utilisateur arrive sur /generate-post
2. Zone de texte libre : "Ton idée en 2 lignes"
   Ex: "J'ai décroché mon premier CDI après 3 mois de galère"
3. Sélection optionnelle : ton (inspirant / expert / authentique)
4. Sélection optionnelle : secteur (auto-détecté depuis le profil)
5. L'IA génère 3 versions en 5 secondes
6. Bouton "Copier" sur chaque version → coller directement sur LinkedIn
7. Bouton "Regénérer" pour obtenir 3 nouvelles versions
```

**Monétisation :**
- Gratuit : 3 posts générés/mois
- Plan Candidat (9,99€) : posts illimités inclus
- Plan Créateur (futur) : historique des posts, analytics, programmation

**Pourquoi c'est différenciant :**
- Pas de prompt à écrire — juste l'idée brute
- Adapté au contexte LinkedIn (pas générique comme ChatGPT)
- Intégré au profil de l'utilisateur (l'IA connaît son secteur, son niveau, son poste visé)
- Interface simple, mobile first, Gen Z

**Backend :**
```
POST /api/generate-post
Body: {
  idee: str,                    # L'idée brute de l'utilisateur
  ton: "inspirant|expert|authentique",  # optionnel
  secteur: str,                 # optionnel, auto-rempli depuis le profil
  poste: str                    # optionnel
}
Response: {
  posts: [
    { ton: "inspirant", contenu: str, hashtags: [...], chars: int },
    { ton: "expert", contenu: str, hashtags: [...], chars: int },
    { ton: "authentique", contenu: str, hashtags: [...], chars: int }
  ]
}
```

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
- Quota freemium affiché en temps réel dans la nav
- Backend auth complet : register/login/me + compteur analyses + historique DB
- SQLite en dev (PostgreSQL Railway en prod)
- Dashboard progression : graphique SVG courbe + 4 stats cards + historique
- stripe_router.py créé avec create-checkout + webhook + subscription-status

### Session 3 — 3 Avril 2026
- ✅ Bug Stripe UnicodeEncodeError corrigé
- ✅ Flow paiement Stripe end-to-end fonctionnel en test
- ✅ Plan mis à jour en DB après paiement (plan: "candidat")
- ✅ Nav affiche "∞ Illimité" en vert pour les abonnés
- ✅ Nouvelle tagline : "Le recruteur t'a vu hier, il t'a zappé. Tu veux qu'on règle ça ?"
- ✅ Nom de domaine link2job.fr acheté chez Ionos
- ✅ Page `create-profile.html` — formulaire guidé 5 étapes style Duolingo/Gen Z

### Session 4 — 4 Avril 2026
- ✅ `utils/ai_agent.py` — fonction `create_profile_from_scratch()` ajoutée
- ✅ `main.py` — endpoint `POST /api/create-profile` branché sur Claude Sonnet
- ✅ Génération IA réelle : détection du genre depuis le prénom
- ✅ Testé end-to-end : `POST /api/create-profile 200 OK` ✅

### Session 5 — 4 Avril 2026
- ✅ Déploiement Railway complet — backend en production
- ✅ PostgreSQL Railway configuré et connecté
- ✅ Variables d'env configurées sur Railway (6 variables)
- ✅ Root Directory `/backend` configuré sur Railway
- ✅ Fix `sqlalchemy` + `psycopg2-binary` + `argon2-cffi` ajoutés au requirements.txt
- ✅ Webhook Stripe prod configuré → Railway
- ✅ `API_URL` mis à jour dans les 3 fichiers frontend → Railway prod
- ✅ Test end-to-end en prod : register ✅ · analyse ✅ · IA ✅
- ✅ `/api/health` → `{"status":"ok","version":"0.2.0"}` ✅

### Commits GitHub
- e9398b2 — initial project structure
- 58637c1 — MVP V1 fonctionnel
- 381fb4c — frontend connecté au backend
- 50b67cc — guide visibilité recruteurs
- ddaceab — auth modal complet
- 8d787da — dashboard progression
- feat: nouvelle tagline hero + page create-profile.html ✅
- feat: backend POST /api/create-profile branché sur Claude Sonnet ✅
- fix: add sqlalchemy and psycopg2 to requirements ✅
- fix: add argon2-cffi for password hashing ✅
- feat: déploiement Railway prod + fix argon2-cffi + API_URL production ✅
- fix: mock parser désactivé + fix HTML hero CTAs structure ✅
- feat: étape 6 guide LinkedIn + modale auth intégrée ✅
- fix: guide 3 titres + bannière IA secteur + badge UX + import Gmail ✅ (dernier)

### Session 6 — 5 Avril 2026
- ✅ DNS Ionos configuré : CNAME www + TXT railway-verify + redirection 301 link2job.fr → www
- ✅ Frontend déployé sur Vercel — link2job.vercel.app live
- ✅ www.link2job.fr → Vercel — Valid Configuration ✅ — SSL ✅
- ✅ Mock parser LinkedIn désactivé → retourne None → force formulaire guidé
- ✅ index.html : les 2 CTAs hero pointent vers create-profile.html
- ✅ create-profile.html : étape 6 "Guide LinkedIn" 8 étapes interactives avec checkboxes
- ✅ Modale auth intégrée dans create-profile.html (register/login avant accès guide)
- ✅ Guide étape 2 : 3 titres avec boutons Copier individuels (Option 1/2/3)
- ✅ Bannière IA : suggestion par secteur avec couleurs + texte + label correct
- ✅ Badge "Suggestion IA" → texte décoratif (fix UX — plus de fausse apparence bouton)
- ✅ Étape G8 connexions : guide import Gmail pas-à-pas avec simulation UI

---

## 🚨 À FAIRE EN SESSION 7 (priorités)

### 1. Générateur de Posts LinkedIn ← PRIORITÉ V2
Implémenter la feature documentée dans "💡 IDÉES PRODUIT" ci-dessus.
- Page `generate-post.html`
- Endpoint `POST /api/generate-post`
- Fonction `generate_linkedin_post()` dans `ai_agent.py`

### 2. Export rapport PDF
Générer un PDF du profil LinkedIn créé (titre + résumé + compétences).
- Librairie : `weasyprint` ou `reportlab` côté backend
- Endpoint : `POST /api/export-profile-pdf`
- Plan Candidat uniquement

### 3. Améliorations guide LinkedIn (étape 6)
- Persistance localStorage : reprendre où on en était si on ferme et revient
- Lien direct depuis dashboard vers le guide de son dernier profil créé

---

## 🏗️ Architecture technique

```
backend/
├── main.py              ← FastAPI
├── auth.py              ← Register/login/me + JWT + argon2
├── database.py          ← SQLAlchemy — User + Analysis models
├── stripe_router.py     ← Stripe checkout + webhook + status
├── Procfile             ← web: uvicorn main:app --host 0.0.0.0 --port $PORT
├── railway.json         ← Config Railway
├── .env                 ← Toutes les clés (jamais commiter)
├── requirements.txt     ← sqlalchemy + psycopg2-binary + argon2-cffi ✅
└── utils/
    ├── linkedin_parser.py  ← DÉSACTIVÉ — retourne None → formulaire guidé ✅
    ├── scorer.py
    └── ai_agent.py         ← analyze_profile() + create_profile_from_scratch() ✅

frontend/
├── index.html           ← Landing + 2 CTAs → create-profile.html + modal auth + Stripe
├── dashboard.html       ← Dashboard progression SVG + historique
├── create-profile.html  ← Formulaire 6 étapes + guide LinkedIn 8 étapes ✅
└── generate-post.html   ← À CRÉER session 7 — Générateur de posts LinkedIn
```

### Endpoints backend actifs (PROD)
```
GET  /api/health                     ✅
POST /api/auth/register              ✅
POST /api/auth/login                 ✅
GET  /api/auth/me                    ✅
POST /api/analyze-profile            ✅ (mock parser)
GET  /api/my-analyses                ✅
POST /api/stripe/create-checkout     ✅
POST /api/stripe/webhook             ✅ (clé prod configurée)
GET  /api/stripe/subscription-status ✅
POST /api/create-profile             ✅ Claude Sonnet réel
POST /api/generate-post              ← À CRÉER session 6
```

### Variables Railway (prod)
```
DATABASE_URL           = ${{Postgres.DATABASE_URL}}
ANTHROPIC_API_KEY      = sk-ant-...
SECRET_KEY             = L2J#xK9mP2qL8nR4vT6wY1uI3oE5aS7d
STRIPE_SECRET_KEY      = sk_test_...
STRIPE_PRICE_ID        = price_1...
STRIPE_WEBHOOK_SECRET  = whsec_... (clé prod Stripe ✅)
```

### ⚠️ Setup dev local (3 terminaux)
```powershell
# Terminal 1 — Backend local
cd C:\Projects\link_to_job\backend
python -m uvicorn main:app --reload

# Terminal 2 — Frontend local
cd C:\Projects\link_to_job\frontend
python -m http.server 5500

# Terminal 3 — Stripe CLI (dev uniquement)
stripe listen --forward-to localhost:8000/api/stripe/webhook
```

### URLs importantes
```
PROD backend  : https://link2job-production.up.railway.app
PROD health   : https://link2job-production.up.railway.app/api/health
DEV frontend  : http://localhost:5500/index.html
DEV dashboard : http://localhost:5500/dashboard.html
DEV profil    : http://localhost:5500/create-profile.html
```

**⚠️ Le frontend pointe sur Railway prod — plus besoin du backend local pour tester**

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

## 🧭 FEATURE À IMPLÉMENTER — Guide LinkedIn Post-Génération

### Contexte
Premier marché = Gen Z, souvent sans profil LinkedIn.
Après génération IA, l'utilisateur ne sait pas quoi faire des textes.
Valeur ajoutée = les guider ENTIÈREMENT de A à Z sur LinkedIn.

### UI — Style identique au guide "Visibilité recruteurs" (déjà dans index.html)
Même composant : numéros cerclés + ligne verticale + simulation UI LinkedIn.
Le guide "Visibilité recruteurs" (guide-step, guide-step-num, sim-ui, sim-radio...) est le modèle exact à réutiliser.

### Étapes du guide (affiché après les résultats dans create-profile.html)

**Étape 1 — Créer ton compte LinkedIn**
→ Va sur linkedin.com/signup
→ Simulation : formulaire LinkedIn (prénom, nom, email, mot de passe)

**Étape 2 — Remplis ton titre professionnel**
→ Profil → "Ajouter un titre"
→ Copie-colle le Titre #1 généré (bouton Copier inline)
→ Simulation UI : champ titre LinkedIn avec le texte pré-rempli

**Étape 3 — Remplis ton résumé (About)**
→ Profil → "Ajouter une section" → "Résumé"
→ Copie-colle le résumé généré
→ ⚠️ Les 3 premières lignes sont visibles sans cliquer "voir plus" — soigne-les

**Étape 4 — Ajoute tes compétences**
→ Profil → "Ajouter une section" → "Compétences"
→ Ajoute les chips générées une par une
→ Simulation : liste des compétences suggérées avec checkbox interactive

**Étape 5 — Ta photo de profil** ← IMPORTANTE Gen Z
→ Photo carrée, fond neutre (blanc, gris, bleu clair)
→ Sourire naturel, cadrage épaules-tête
→ Pas de selfie bras tendu, pas de filtre, pas de photo de groupe
→ 💡 Astuce : prends-la en lumière naturelle face à une fenêtre

**Étape 6 — Ta bannière LinkedIn** ← DIFFÉRENCIANT
→ C'est la grande image en haut du profil (1584 x 396px)
→ La plupart laissent la bannière par défaut = profil fade et invisible
→ Suggestions selon le secteur :
   - Tech/Data : fond sombre avec code ou circuit
   - Marketing : couleurs vives, accroche courte
   - Finance : sobre, bleu marine
→ 💡 Canva gratuit : templates "LinkedIn Banner"
→ Future feature : génération automatique de bannière par IA selon le profil

**Étape 7 — Visibilité recruteurs** ← déjà buildé dans index.html !
→ Réutiliser exactement le guide "Open to Work" existant
→ Sélectionner "Recruteurs uniquement" et pas "Tous les membres LinkedIn"

**Étape 8 — Envoie 3 demandes de connexion**
→ Commence par tes profs, camarades de classe, famille pro
→ Un profil avec 0 connexion est invisible de l'algorithme LinkedIn
→ Objectif : 50 connexions dans la première semaine

### Composant à créer
- Section supplémentaire dans `create-profile.html` après l'étape 5 résultats IA
- OU page dédiée `frontend/guide-linkedin.html` avec lien depuis les résultats
- Même style CSS que le guide visibilité (guide-step, guide-step-num, sim-ui...)
- Boutons "Copier" inline pour chaque texte généré à l'étape correspondante
- Progress bar : "Tu as complété X/8 étapes de ton profil LinkedIn"
- Chaque étape se coche quand l'utilisateur clique "C'est fait ✓"
- Persistance de l'état via localStorage (l'utilisateur peut reprendre plus tard)

### Pourquoi c'est la killer feature
- La Gen Z veut être guidée, pas juste informée — elle abandonne si c'est flou
- Aucun concurrent ne fait ça — ils donnent les textes et basta
- Taux de complétion = métrique clé → utilisateur qui complète = utilisateur qui revient
- Chaque étape complétée = micro-victoire = engagement émotionnel fort
- La bannière personnalisée = WOW effect = partage organique spontané
- Ce guide = argument de vente direct pour le plan Candidat (accès guide complet)

### Priorité
Session 7 ou 8 — après le Générateur de Posts LinkedIn (session 6/7)

---

## 🗺️ Feuille de route

### V1 — "Le Profil Parfait" ← SESSION 6 TERMINÉE ✅
- [x] Landing page complète
- [x] Analyse IA Claude Sonnet — score + recommandations + textes
- [x] Auth register/login JWT + 3 analyses gratuites
- [x] Dashboard progression SVG + historique
- [x] Stripe checkout + webhook ✅
- [x] create-profile.html — formulaire 6 étapes + guide LinkedIn ✅
- [x] Backend POST /api/create-profile Claude Sonnet ✅
- [x] Déploiement Railway production ✅
- [x] LinkedIn parser mock désactivé → formulaire guidé ✅
- [x] www.link2job.fr → Vercel ✅
- [x] link2job.fr → redirection → www.link2job.fr ✅
- [ ] Export rapport PDF ← SESSION 7

### V2 — "La Présence LinkedIn" ← NOUVELLE VISION
- [ ] **Générateur de posts LinkedIn** ← Feature prioritaire V2
- [ ] Historique des posts générés
- [ ] Analytics posts (portée estimée, score d'engagement)
- [ ] Programmation de posts (scheduler)
- [ ] Extension Chrome Manifest V3
- [ ] CV uploadé → moteur ATS cv-ats-ready
- [ ] Lettre de motivation IA contextuelle

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
| Gratuit | 0€ | 3 analyses + 3 posts générés/mois |
| Candidat | 9,99€/mois | Analyses + posts illimités |
| Candidat Pro | 19,99€/mois | + Extension Chrome + suivi |
| Grande École | 500-2000€/an | Licence B2B |
| Employeur | 99-299€/mois | Tableau de bord V3 |

### Arguments pitch 9,99€
```
Coût par abonné/mois :
  Claude Sonnet (10 analyses + 20 posts) ≈ 0,50€
  Hébergement Railway                    ≈ 0,05€
  Stripe commission                      ≈ 0,35€
  ───────────────────────────────────────────────
  Total coût                             ≈ 0,90€
  Marge nette                            ≈ 9,09€ (91%)

Ne jamais baisser le prix affiché.
```

---

## 🧠 Décisions produit importantes

- **LinkedIn parser = DÉSACTIVÉ** → retourne None → redirige vers create-profile.html (formulaire guidé)
- **Proxycurl / scraping LinkedIn = NON** → LinkedIn a gagné en justice contre les scrapers
- **3 analyses gratuites** = inscription obligatoire (capture email + anti-abus)
- **Générateur posts** = même logique que cv-ats-ready.fr — automatiser ce que les gens font manuellement sur ChatGPT
- **Posts LinkedIn** = pas de prompt à écrire, juste l'idée brute → 3 versions générées
- **Dashboard = produit payant** — progression dans le temps justifie l'abo
- **Stripe CLI** = obligatoire en dev pour les webhooks locaux
- **En prod** : webhook Stripe configuré sur Railway ✅
- **link2job.fr** → redirection Ionos 301 → www.link2job.fr → Vercel ✅
- **Frontend** = Vercel (www.link2job.fr) ✅
- **Backend** = Railway prod (link2job-production.up.railway.app) ✅
- **Railway projet** : link2job / ID : a1cdcce4-545c-4abc-8d48-9169272d3489
- **Guide LinkedIn** = étape 6 dans create-profile.html — 8 étapes interactives avec checkboxes
- **Auth avant guide** = modale register/login s'ouvre au clic "Guide moi" si non connecté
- **Badge décoratif** = ne jamais mettre un élément visuellement cliquable sans action réelle
