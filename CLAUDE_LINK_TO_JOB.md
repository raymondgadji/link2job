# CLAUDE.md — LINK TO JOB
> Mémoire projet complète. À coller en début de chaque nouvelle session.
> Objectif : N°1 européen de la recherche d'emploi et de stage automatisée par IA.

---

## 🎯 Vision produit

**LINK TO JOB** — L'app qui trouve ton emploi pendant que tu dors.
**Tagline** : "Tu te connectes une fois. On s'occupe de ta carrière."
**URL cible** : linktojob.fr (à acheter)
**Rôles** : Founder (utilisateur) + CTO (Claude)

### Mission
Démocratiser l'accès à l'emploi pour tous — du lycéen de 16 ans qui cherche son premier stage jusqu'au cadre en reconversion — grâce à l'automatisation intelligente et éthique de la recherche d'emploi sur LinkedIn, puis sur tous les réseaux.

### Positionnement
Pas un spammeur de candidatures comme LazyApply.
Un **candidat augmenté** — qualité, personnalisation, accord du candidat à chaque action.
La différence : on optimise D'ABORD le profil, ENSUITE on candidate intelligemment.

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

## 🏗️ Architecture technique (cible)

| Couche | Techno | Raison |
|--------|--------|--------|
| Frontend web | HTML/CSS/JS (même stack cv-ats-ready) | Cohérence, rapidité |
| Extension Chrome | JavaScript (Manifest V3) | Accès LinkedIn sans API officielle |
| Backend | Python FastAPI | Même stack maîtrisée |
| IA | Claude API (Sonnet pour analyse, Haiku pour génération) | Puissance + coût |
| Auth | JWT + OAuth LinkedIn (si dispo) | Sécurité |
| DB | PostgreSQL (Railway) | Persistance données candidatures |
| Paiement | Stripe | Même intégration que cv-ats-ready |
| Analytics | Umami + logs custom | RGPD compliant |

---

## 🎨 Charte graphique (identique cv-ats-ready)

```
⚠️ MÊME DESIGN SYSTEM QUE CV-ATS-READY — cohérence écosystème

Primaire :       #FF6B00 (orange vif)
Primaire foncé : #D95A00
Fond sombre :    #0C0C18 / #1A1A2E
Fond clair :     #FAFAF8
Succès :         #22C55E
Erreur :         #EF4444
Accent bleu :    #0A66C2 (couleur LinkedIn — utilisé pour les éléments LinkedIn)

Typo titres :    Syne 800
Typo corps :     DM Sans
Border radius :  sm=8px md=14px lg=22px xl=32px

Effets :         Glassmorphism, orbs animés, noise texture, gradients orange
Émotion :        "Apple-like" — chaque pixel compte, chaque animation a un but
```

---

## 🗺️ Feuille de route produit

### V1 — "Le Profil Parfait" (MVP — 4-6 semaines)
> Web app uniquement. Pas encore d'extension Chrome.
> Objectif : analyser et optimiser le profil LinkedIn du candidat.

**Fonctionnalités :**
- [ ] Landing page LINK TO JOB (2 portails : Candidat / Employeur)
- [ ] Connexion candidat (email + mot de passe)
- [ ] Import profil LinkedIn par URL publique
- [ ] Analyse IA du profil (Claude API) :
  - Titre professionnel — optimisation mots-clés
  - Résumé (About) — premières lignes cruciales
  - Photo de profil — checklist qualité
  - Compétences — sélection stratégique
  - Recommandations — manquantes ou présentes
  - Activité LinkedIn — fréquence et qualité
  - Mode "Open to Work" — conseils stratégiques
- [ ] Score de profil LinkedIn avant/après (0-100)
- [ ] Textes optimisés générés par IA (titre, résumé) — copier-coller
- [ ] Rapport PDF téléchargeable
- [ ] Modèle freemium : 3 analyses gratuites puis 9,99€/mois

### V2 — "La Candidature Intelligente" (Extension Chrome — 6-10 semaines)
> Extension Chrome qui agit avec l'accord de l'utilisateur.

**Fonctionnalités :**
- [ ] Extension Chrome installable (Manifest V3)
- [ ] Connexion à son compte LinkedIn via l'extension
- [ ] Détection automatique des offres qui matchent le profil
- [ ] Score de compatibilité offre/profil (IA)
- [ ] Candidature en 1 clic avec personnalisation automatique
- [ ] Message de connexion personnalisé généré par IA
- [ ] Accord explicite du candidat avant chaque action
- [ ] Dashboard de suivi des candidatures (envoyées, vues, réponses)
- [ ] Relance automatique intelligente

### V3 — "L'Écosystème Emploi" (Multi-plateformes — 3-6 mois)
- [ ] Volet Employeur (tableau de bord recruteur, accès profils optimisés)
- [ ] Extension vers Indeed, Welcome to the Jungle, France Travail
- [ ] Licences B2B grandes écoles (HEC, ESSEC, EmLyon...)
- [ ] API LINK TO JOB pour intégrations tierces
- [ ] App mobile iOS/Android

---

## 👥 Marchés cibles (par priorité)

### Marché 1 — Les jeunes (16-25 ans)
Lycéens, étudiants cherchant premier emploi, stage, alternance.
Pain point : ne savent pas comment optimiser leur présence LinkedIn.
Acquisition : TikTok, Instagram, bouche-à-oreille.
Prix : Freemium agressif.

### Marché 2 — Grandes écoles françaises
HEC, ESSEC, INSEAD, EmLyon, Sciences Po, etc.
Pain point : accompagnement carrière insuffisant, pression placement.
Acquisition : B2B direct, partenariats bureaux des étudiants (BDE).
Prix : Licence institution 500-2000€/an.

### Marché 3 — Demandeurs d'emploi
Personnes en reconversion, chômeurs, cadres en transition.
Pain point : découragement, manque de méthode, profil LinkedIn non optimisé.
Acquisition : France Travail partenariats, SEO "optimiser profil LinkedIn".
Prix : 9,99-19,99€/mois.

### Marché 4 — Employeurs (V3)
PME, startups, RH cherchant des profils qualifiés.
Pain point : trop de candidatures non pertinentes, coût des ATS.
Prix : 99-299€/mois.

---

## 💰 Modèle économique

| Plan | Prix | Inclus |
|------|------|--------|
| Gratuit | 0€ | 3 analyses profil, score LinkedIn |
| Candidat | 9,99€/mois | Analyses illimitées + textes IA |
| Candidat Pro | 19,99€/mois | + Extension Chrome + suivi candidatures |
| Grande École | 500-2000€/an | Licence multi-utilisateurs B2B |
| Employeur | 99-299€/mois | Accès profils + tableau de bord (V3) |

**Projection conservatrice :**
```
100 abonnés Candidat (9,99€)  = 999€/mois
10 abonnés Pro (19,99€)       = 200€/mois
1 licence école (1000€/an)    = 83€/mois
→ Total mois 3 : ~1300€ MRR
```

---

## 🏆 Analyse concurrentielle

| Concurrent | Forces | Faiblesses | Notre avantage |
|------------|--------|------------|----------------|
| LazyApply | Extension Chrome populaire | Spam, pas de personnalisation, US-centric | Qualité + marché FR |
| LoopCV | Multi-plateformes | UX complexe, pas d'optimisation profil | UX Apple-like + profil |
| Sorce.jobs | Matching IA | Pas d'automatisation active | Action + suivi |
| LinkedIn Premium | Crédibilité | 40€/mois, pas d'automatisation | Prix + action réelle |
| Huntr | Suivi candidatures | Manuel, pas d'IA | Automatisation totale |

**Fenêtre d'opportunité :** Aucun acteur français dominant. Pas de solution qui combine optimisation profil + candidature intelligente + accord utilisateur + double marché dans une UX premium.

---

## ⚠️ Risques et mitigation

### Risque 1 — CGU LinkedIn (CRITIQUE)
LinkedIn interdit le scraping et l'automatisation dans ses CGU.
**Mitigation V1 :** Analyse de profil public uniquement (URL publique) — 100% légal.
**Mitigation V2 :** Extension Chrome qui simule les actions humaines — zone grise mais standard industrie (LazyApply, Dux-Soup font ça depuis des années).
**Mitigation long terme :** Partenariat LinkedIn officiel quand on a la traction.

### Risque 2 — Confiance utilisateur
Donner accès à son LinkedIn = acte de confiance énorme.
**Mitigation :** Accord explicite avant chaque action. Zéro stockage des credentials. Audit sécurité. Mentions légales claires.

### Risque 3 — Dépendance LinkedIn
Si LinkedIn change ses règles, l'extension peut être bloquée.
**Mitigation :** Diversification vers d'autres plateformes dès la V3.

### Risque 4 — Complexité technique extension Chrome
Manifest V3 est plus restrictif que V2.
**Mitigation :** Commencer par la web app V1 (zéro risque) avant l'extension.

---

## 🛠️ Stack de développement

### Dossier projet (à créer)
```
C:\Projects\link_to_job\
├── frontend/
│   └── index.html             ← Landing page + app web
├── backend/
│   ├── main.py                ← FastAPI
│   ├── utils/
│   │   ├── linkedin_parser.py ← Parsing profil LinkedIn public
│   │   ├── ai_agent.py        ← Analyse et génération Claude API
│   │   └── scorer.py          ← Score profil LinkedIn
│   ├── .env
│   └── requirements.txt
├── extension/                 ← V2 uniquement
│   ├── manifest.json
│   ├── popup.html
│   ├── content.js
│   └── background.js
└── CLAUDE.md
```

### Requirements backend (V1)
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
python-multipart==0.0.9
anthropic==0.86.0
stripe==10.12.0
httpx==0.27.0          ← Pour scraping profil LinkedIn public
beautifulsoup4==4.12.0 ← Parsing HTML LinkedIn
python-dotenv==1.0.0
psycopg2-binary==2.9.9 ← PostgreSQL
python-jose==3.3.0     ← JWT auth
passlib==1.7.4         ← Password hashing
```

---

## 📐 Pages et flux utilisateur (V1)

### Landing page
- Hero : "LinkedIn travaille pour toi, pas l'inverse"
- 2 portails : [Je suis candidat] [Je suis employeur]
- How it works en 3 étapes
- Témoignages (à construire pendant bêta)
- Pricing
- FAQ

### Flux Candidat V1
1. Inscription email
2. Colle ton URL LinkedIn publique
3. L'IA analyse ton profil (30 sec)
4. Score affiché : avant XX% → objectif XX%
5. Recommandations détaillées par section
6. Textes optimisés générés (titre, résumé)
7. Télécharge le rapport PDF
8. Upgrade pour accès illimité

### Flux Employeur (V3)
1. Inscription entreprise
2. Décrit le poste recherché
3. Accès aux profils LINK TO JOB optimisés qui matchent
4. Contact direct ou invitation à postuler

---

## 🔌 Endpoints backend (V1 cible)

```
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me

POST /api/analyze-profile       ← URL LinkedIn → analyse IA complète
GET  /api/profile/:id           ← Récupère analyse sauvegardée
GET  /api/profile/:id/report    ← Génère PDF rapport

POST /api/create-subscription   ← Stripe subscription
POST /api/webhook/stripe

GET  /api/admin/logs?secret=XXX
GET  /api/health
```

---

## 🎯 KPIs à tracker

```
Candidats inscrits (total)
Analyses de profil effectuées
Taux conversion gratuit → payant
MRR (Monthly Recurring Revenue)
Score LinkedIn moyen avant/après
NPS (satisfaction utilisateur)
```

---

## 📋 Prochaines tâches immédiates

### PHASE 0 — Fondations (cette semaine)
- [ ] Acheter domaine linktojob.fr sur OVH/Ionos
- [ ] Créer dossier C:\Projects\link_to_job\
- [ ] Initialiser repo GitHub privé "link-to-job"
- [ ] Créer environnement venv Python

### PHASE 1 — Landing page + analyse profil (semaines 1-2)
- [ ] Landing page HTML avec 2 portails (même charte cv-ats-ready)
- [ ] Backend FastAPI avec endpoint /api/analyze-profile
- [ ] Parsing profil LinkedIn public (httpx + BeautifulSoup)
- [ ] Prompt Claude pour analyse et scoring profil
- [ ] Affichage résultats avec score avant/après
- [ ] Export rapport PDF

### PHASE 2 — Auth + Freemium (semaines 3-4)
- [ ] Système auth (inscription/connexion)
- [ ] Intégration Stripe (abonnement mensuel)
- [ ] Dashboard utilisateur (historique analyses)
- [ ] 3 analyses gratuites puis payant

### PHASE 3 — Extension Chrome (semaines 5-8)
- [ ] Extension Chrome Manifest V3
- [ ] Détection offres LinkedIn matchantes
- [ ] Candidature 1 clic avec accord utilisateur
- [ ] Suivi candidatures

---

## 📝 Wording validé

```
Tagline principale : "Tu te connectes une fois. On s'occupe de ta carrière."
Tagline courte : "LinkedIn travaille pour toi, pas l'inverse."
CTA principal : "Optimiser mon profil LinkedIn →"
CTA secondaire : "Voir comment ça marche"
Copyright : © 2026 linktojob.fr
Footer : "Fait avec ❤️ pour tous ceux qui méritent mieux"
```

---

## 🏢 Structure juridique
Même SASU que cv-ats-ready (à créer).
Les deux produits sous la même entité juridique = cohérence Station F.
