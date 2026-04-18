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

### 🔥 Skill 1 — Trend Research ← SESSION 11/12

**Insight :** Zeyneb MADI a multiplié ses followers x10 avec ce système. L'idée : au lieu que l'utilisateur cherche quoi écrire, on lui propose directement 5 sujets chauds dans son secteur cette semaine.

**Ce que ça change dans generate-post.html :**
Avant même que l'utilisateur tape quoi que ce soit, une section **"💡 Idées tendance cette semaine"** affiche 5 sujets chauds dans son secteur. Il clique → ça pré-remplit la zone de texte → il génère. Zéro friction, zéro page blanche.

**Flow utilisateur :**
```
1. L'utilisateur arrive sur /generate-post
2. NOUVEAU : Section "Tendances cette semaine en [son secteur]"
   → 5 sujets proposés sous forme de chips cliquables
   Ex (Tech) : "Le débat sur Cursor vs Copilot" / "Les layoffs Amazon 2026" / "React 19 — ce qui change"
3. Il clique sur un sujet → pré-remplit la zone "Ton idée"
4. Flow normal : ton → générer → copier
```

**Stack technique :**
- Backend : `GET /api/trending-topics?secteur=Tech` 
- Appel web search (Brave Search API ou Tavily) sur Reddit/X/LinkedIn des 7 derniers jours
- Claude résume et formate en 5 sujets actionnables pour le secteur
- Cache 24h en DB pour ne pas surcharger l'API search
- Fallback : sujets statiques par secteur si l'API search est down

**Fichiers à modifier :**
- `backend/utils/ai_agent.py` → nouvelle fonction `get_trending_topics(secteur)`
- `backend/main.py` → endpoint `GET /api/trending-topics`
- `frontend/generate-post.html` → section tendances avant la zone de texte

**Priorité :** Session 11 ou 12 — après quota posts dashboard (session 10)

---

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

### Session 8 — 16 Avril 2026
- ✅ `generate-post.html` — page frontend générateur de posts LinkedIn V2
  - Zone de texte idée libre + compteur caractères
  - Sélection ton : Les 3 / 🔥 Inspirant / 🎯 Expert / 💚 Authentique
  - Contexte optionnel : secteur + poste
  - Loading animé 4 étapes
  - 3 cards résultats avec hook visible + expand "Voir le post complet"
  - Bouton Copier sur chaque card + bouton Regénérer
- ✅ Navigation complète entre toutes les pages (index, create-profile, generate-post, dashboard)
- ✅ Dashboard : 2 quick-access cards en haut (Créer profil + Générer post)
- ✅ Backend `POST /api/generate-post` — 3 posts (inspirant/expert/authentique) ✅
- ✅ Quota posts : 3 gratuits/mois, reset le 1er du mois, illimité plan Candidat
- ✅ `generate-post.html` connecté à la nav de toutes les pages

### Session 9 — 18 Avril 2026
- ✅ **Historique posts dans le dashboard**
  - Modèle `Post` dans `database.py` (id, user_id, idee, ton, secteur, contenu JSON, created_at)
  - Migration douce : colonnes `posts_used` et `posts_reset_date` ajoutées si absentes
  - Sauvegarde automatique dans `/api/generate-post` après chaque génération
  - Endpoint `GET /api/my-posts` — retourne les 20 derniers posts
  - `dashboard.html` — `renderPosts()` : idée tronquée + pill ton coloré + date + hook + bouton Copier
- ✅ **Warning VS Code ligne 121** — `-webkit-line-clamp` : warning cosmétique ignoré (pas une erreur)
- ✅ **2 nouveaux secteurs** dans `create-profile.html` :
  - **Cybersécurité** : skills (Pentest, SIEM, Kali Linux, ISO 27001, SOC…) + conseil photo + bannière vert matrix
  - **Responsable Réseaux Sociaux** : skills (Meta Business Suite, Hootsuite, TikTok Ads…) + conseil photo + bannière violet/rose
  - 4 zones mises à jour : `<select>`, `HARD_SUGGESTIONS`, `PHOTO_ADVICE`, `BANNER_SUGGESTIONS`
  - `ai_agent.py` : **aucune modification nécessaire** (secteur passé en texte libre dans le prompt)
- ✅ **Commits session 9** :
  ```
  feat: historique posts dans dashboard + endpoint /api/my-posts
  feat: ajout secteurs Cybersécurité et Responsable Réseaux Sociaux
  ```

---

## 🗂️ Architecture technique

### Stack
```
Frontend  : HTML/CSS/JS vanilla — Vercel (www.link2job.fr)
Backend   : FastAPI Python — Railway (link2job-production.up.railway.app)
DB dev    : SQLite (fichier local link2job.db)
DB prod   : PostgreSQL Railway
Auth      : JWT (python-jose) + argon2 hashing
IA        : Claude Sonnet 4 (claude-sonnet-4-20250514) via Anthropic SDK
Paiement  : Stripe (checkout + webhook)
```

### Fichiers clés
```
backend/
  main.py           → FastAPI app, tous les endpoints
  database.py       → modèles SQLAlchemy (User, Analysis, Post)
  auth.py           → JWT, register/login, quotas freemium
  stripe_router.py  → checkout, webhook, subscription-status
  utils/
    ai_agent.py     → analyze_profile() + create_profile_from_scratch() + generate_linkedin_post()
    scorer.py       → compute_score() — score LinkedIn 0-100
    linkedin_parser.py → désactivé (retourne None → redirect create-profile)

frontend/
  index.html          → Landing page + hero analyse + résultats IA
  create-profile.html → Formulaire 6 étapes + guide LinkedIn 8 étapes
  generate-post.html  → Générateur posts LinkedIn 3 tons
  dashboard.html      → Dashboard progression + historique analyses + historique posts
```

### Endpoints API
```
GET  /api/health                → {"status":"ok","version":"0.4.0"}
POST /api/auth/register         → inscription JWT
POST /api/auth/login            → connexion JWT
GET  /api/auth/me               → profil utilisateur courant
POST /api/analyze-profile       → analyse URL LinkedIn (désactivée → 422)
POST /api/create-profile        → génération profil IA depuis formulaire
POST /api/generate-post         → génération 3 posts LinkedIn IA
GET  /api/my-analyses           → historique analyses de l'utilisateur
GET  /api/my-posts              → historique posts générés (20 derniers)
POST /api/stripe/create-checkout → session Stripe
POST /api/stripe/webhook        → événements Stripe
GET  /api/stripe/subscription-status → statut abonnement
```

### Modèles DB
```python
User     : id, email, hashed_password, full_name, is_active, plan,
           analyses_used, posts_used, posts_reset_date, created_at
Analysis : id, user_id, linkedin_url, score_before, score_details (JSON), created_at
Post     : id, user_id, idee, ton, secteur, contenu (JSON), created_at
```

### Quotas freemium
```
Analyses : 3 gratuites → illimitées plan Candidat+
Posts    : 3/mois gratuits, reset le 1er du mois → illimités plan Candidat+
```

---

## 🗺️ Feuille de route

### V1 — "Le Profil Parfait" ✅ TERMINÉE — 8 Avril 2026
- [x] Landing page complète
- [x] Analyse IA Claude Sonnet — score + recommandations + textes
- [x] Auth register/login JWT + 3 analyses gratuites
- [x] Dashboard progression SVG + historique
- [x] Stripe checkout + webhook ✅
- [x] create-profile.html — formulaire 6 étapes + guide LinkedIn 8 étapes ✅
- [x] Backend POST /api/create-profile Claude Sonnet ✅
- [x] POST /api/generate-post — 3 posts LinkedIn (inspirant/expert/authentique) ✅
- [x] Déploiement Railway production ✅
- [x] www.link2job.fr → Vercel ✅
- [x] UX Mobile Gen Z — stories swipe + micro-animations + retour navigateur ✅
- [x] 15 secteurs couverts — hard skills + photo + bannière IA ✅ (dont Cybersécurité + Réseaux Sociaux ajoutés S9)

### 🎯 MODE ACQUISITION — Maintenant
- [ ] Envoyer à 10-20 personnes du réseau (famille, amis, EmLyon)
- [ ] Collecter les feedbacks (qu'est-ce qui bloque ? qu'est-ce qu'ils adorent ?)
- [ ] Poster sur LinkedIn (Raymond) — storytelling du projet
- [ ] Poster sur les groupes Facebook/Discord emploi/stage
- [ ] Objectif : 50 utilisateurs inscrits + 5 feedbacks détaillés

### V2 — "La Présence LinkedIn" ← EN COURS
- [x] **Page generate-post.html** ← Frontend générateur de posts ✅
- [x] Navigation complète entre toutes les pages ✅
- [x] Dashboard accès rapide 2 features ✅
- [x] **Historique des posts générés dans le dashboard** ✅ SESSION 9
- [x] **Secteurs Cybersécurité + Responsable Réseaux Sociaux** ✅ SESSION 9
- [ ] Quota posts affiché dans le dashboard (posts_used / posts_remaining) ← SESSION 10
- [ ] Analytics posts (portée estimée, score d'engagement)
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

### Plans (mis à jour V2)
| Plan | Prix | Inclus |
|------|------|--------|
| Gratuit | 0€ | 1 profil LinkedIn IA + 3 posts/mois + guide 8 étapes + score LinkedIn |
| Candidat | 9,99€/mois | Tout Gratuit + profils & posts illimités + analyses illimitées + historique |
| Candidat Pro | 19,99€/mois | Tout Candidat + Extension Chrome V3 + agent candidature auto + suivi + relance |
| Grande École | 500-2000€/an | Licence B2B |
| Employeur | 99-299€/mois | Tableau de bord V3 |

### Règle d'inclusion (IMPORTANT)
```
Gratuit ⊂ Candidat ⊂ Candidat Pro
```
Chaque plan supérieur inclut TOUT ce que fait le plan inférieur.
Affiché en première ligne de chaque plan : "✓ Tout le plan X inclus" en orange.

### Analyse de rentabilité (Claude Sonnet 4)
```
Coût Claude par action :
  create-profile  : ~800 input + ~600 output tokens  = 0,01€
  generate-post   : ~600 input + ~1500 output tokens = 0,02€

Scénario heavy user Candidat (20 profils + 50 posts/mois) :
  Coût Claude     : 0,20€ + 1,00€ = 1,20€
  Railway         : 0,05€
  Stripe (3,5%)   : 0,35€
  ─────────────────────────────────
  Total coûts     : 1,60€
  Revenu          : 9,99€
  Marge brute     : 8,39€ (84%) ✅

Auto-entrepreneur (charges ~22%) :
  100 abonnés  → ~619€ net/mois
  500 abonnés  → ~3 095€ net/mois
  1000 abonnés → ~6 190€ net/mois

Ne jamais baisser le prix affiché.
Le vrai défi = acquisition, pas les coûts.
```

---

## 🧠 Décisions produit importantes

- **LinkedIn parser = DÉSACTIVÉ** → retourne None → redirige vers create-profile.html (formulaire guidé)
- **Proxycurl / scraping LinkedIn = NON** → LinkedIn a gagné en justice contre les scrapers
- **3 analyses gratuites** = inscription obligatoire (capture email + anti-abus)
- **Export PDF = ABANDONNÉ** → pas de valeur ajoutée vs boutons Copier existants
- **Générateur posts** = même logique que cv-ats-ready.fr — backend déjà prêt en v0.3.0, frontend V2
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
- **Pricing** = Gratuit ⊂ Candidat ⊂ Candidat Pro — inclusion explicite en première ligne de chaque plan
- **Marge brute** = 84% — le coût technique ne sera jamais un problème, le vrai défi c'est l'acquisition
- **cv-ats-ready.fr** = à intégrer en V3 uniquement — l'agent aura besoin du CV optimisé ATS pour postuler
- **generate-post.html** = page frontend V2 ✅ — 3 tons, expand/collapse, copier, regénérer
- **Navigation** = toutes les pages connectées entre elles ✅
- **Dashboard** = accès rapide 2 features en cards en haut ✅
- **HoloTab / H Company** = concurrent généraliste — nous spécialisé emploi/LinkedIn, avantage = contexte utilisateur connu
- **V3 agent** = prendra le contrôle du navigateur pour postuler automatiquement — spécialisé emploi
- **ai_agent.py secteurs** = aucune modification nécessaire pour nouveaux secteurs — passés en texte libre dans le prompt
- **Warning VS Code `-webkit-line-clamp`** = cosmétique uniquement, pas une erreur fonctionnelle
- **Historique posts** = sauvegardé en DB à chaque génération, affiché dans dashboard (20 derniers)
