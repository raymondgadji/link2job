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

## ✅ CE QUI A ÉTÉ BUILDÉ (Session 1 — 2 Avril 2026)

### Commits GitHub
- `feat: initial project structure — Link2Job` (e9398b2)
- `feat: MVP V1 fonctionnel — landing page + backend FastAPI + analyse IA LinkedIn` (58637c1)
- `feat: frontend connecté au backend — formulaire + résultats IA complets` (381fb4c)
- Guide Visibilité recruteurs → à commiter (index.html modifié, non pushé encore)

### Frontend — `frontend/index.html`
Landing page complète avec :
- Nav fixe glassmorphism
- Hero avec formulaire LinkedIn (input URL + bouton "Analyser mon profil")
- Deuxième phrase hero : "Pas encore de profil LinkedIn ? On te le crée de zéro. ✨"
- Loading animé 4 étapes (Récupération → Analyse IA → Génération → Score)
- **Section Résultats complète** :
  - Score ring SVG animé 0-100 avec counter
  - Mini-barres par section colorées (vert/orange/rouge selon score)
  - Cards recommandations IA (priorité haute/moyenne/basse)
  - 3 titres LinkedIn optimisés + bouton Copier
  - Résumé About complet généré + bouton Copier
  - **Guide interactif "Visibilité recruteurs"** (toggle, 5 étapes, simulation UI LinkedIn)
- Stats, How it works, Features, Pricing (Free/9,99€/19,99€), Témoignages, FAQ, Footer

### Backend — `backend/`
```
backend/
├── main.py              ← FastAPI, endpoints /api/health + /api/analyze-profile
├── .env                 ← ANTHROPIC_API_KEY (ne jamais commiter)
├── .env.example         ← Template
├── requirements.txt
└── utils/
    ├── __init__.py
    ├── linkedin_parser.py  ← Mock actif (retourne profil Raymond Gadji)
    ├── scorer.py           ← Score 0-100 par section (8 critères pondérés)
    └── ai_agent.py         ← Claude Sonnet — analyse + génération textes
```

### Décisions techniques prises
- **LinkedIn parser = MOCK en dev** — LinkedIn bloque le scraping. Solution prod = Proxycurl API (~$0.01/profil)
- **"Open to Work" = déconseillé** — on conseille "Recruteurs uniquement" partout
- **3 analyses gratuites** = 3 analyses du MÊME profil (cycle amélioration : analyser → appliquer → re-analyser)
- **Clé API Anthropic** : créer une clé dédiée "link2job-dev" dans console.anthropic.com pour séparer les coûts de cv-ats-ready

---

## 🏗️ Architecture technique (cible)

| Couche | Techno | Raison |
|--------|--------|--------|
| Frontend web | HTML/CSS/JS | Cohérence, rapidité |
| Extension Chrome | JavaScript (Manifest V3) | Accès LinkedIn sans API officielle |
| Backend | Python FastAPI | Stack maîtrisée |
| IA | Claude API (Sonnet analyse, Haiku génération) | Puissance + coût |
| Auth | JWT + OAuth LinkedIn | Sécurité |
| DB | PostgreSQL (Railway) | Persistance |
| Paiement | Stripe | Même intégration cv-ats-ready |
| Analytics | Umami + logs custom | RGPD compliant |

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

## 🗺️ Feuille de route produit

### V1 — "Le Profil Parfait" ← ON EST ICI
- [x] Landing page complète
- [x] Formulaire analyse LinkedIn connecté au backend
- [x] Analyse IA (Claude Sonnet) — score + recommandations + textes
- [x] Guide interactif "Visibilité recruteurs"
- [ ] **Proxycurl API** — remplacer le mock par le vrai parsing LinkedIn
- [ ] **Système auth** — inscription/connexion + compteur 3 analyses gratuites
- [ ] **Dashboard progression** — historique des scores dans le temps
- [ ] **Intégration Stripe** — abonnement 9,99€/mois
- [ ] **Export rapport PDF**

### V2 — "La Candidature Intelligente" (Extension Chrome)
- [ ] Extension Chrome Manifest V3
- [ ] Candidature 1 clic avec accord utilisateur
- [ ] **CV uploadé** → moteur ATS de cv-ats-ready (réutiliser les fichiers existants)
- [ ] **Lettre de motivation générée par IA** contextuelle à l'offre
  - Question "Tu veux ajouter quelque chose ?" avant envoi
  - Raymond partagera tous les fichiers cv-ats-ready quand on code ça
- [ ] Dashboard suivi candidatures
- [ ] Relance automatique intelligente

### V3 — "L'Écosystème Emploi"
- [ ] Volet Employeur
- [ ] Extension vers Indeed, Welcome to the Jungle, France Travail
- [ ] Licences B2B grandes écoles
- [ ] App mobile iOS/Android

---

## 📐 Prochaines tâches (par priorité)

### Immédiat
1. **Commiter le guide Visibilité recruteurs** (index.html modifié non pushé)
2. **Proxycurl API** — vrai parsing LinkedIn (remplace le mock)
3. **Système auth** — inscription/connexion, compteur 3 analyses gratuites

### Ensuite
4. Dashboard progression (historique scores)
5. Stripe abonnement
6. Export PDF rapport

---

## 💰 Modèle économique

| Plan | Prix | Inclus |
|------|------|--------|
| Gratuit | 0€ | 3 analyses de profil (même profil, cycle amélioration) |
| Candidat | 9,99€/mois | Analyses illimitées + textes IA |
| Candidat Pro | 19,99€/mois | + Extension Chrome + suivi candidatures |
| Grande École | 500-2000€/an | Licence multi-utilisateurs B2B |
| Employeur | 99-299€/mois | Accès profils + tableau de bord (V3) |

---

## ⚠️ Risques et mitigation

### Risque 1 — CGU LinkedIn (CRITIQUE)
**Mitigation V1 :** Proxycurl API (légal, ils gèrent la conformité).
**Mitigation V2 :** Extension Chrome simule actions humaines (standard industrie).

### Risque 2 — Confiance utilisateur
**Mitigation :** Accord explicite avant chaque action. Zéro stockage credentials.

---

## 🔌 Endpoints backend (V1 actuel)

```
GET  /api/health
POST /api/analyze-profile   ← URL LinkedIn → score + recommandations + textes IA
```

---

## 📝 Wording validé

```
Tagline principale : "Tu te connectes une fois. On s'occupe de ta carrière."
Tagline courte : "LinkedIn travaille pour toi, pas l'inverse."
Hero phrase 1 : "Tu te connectes une fois. Link2Job analyse ton profil, l'optimise, et candidate pour toi — avec ton accord à chaque étape."
Hero phrase 2 : "Pas encore de profil LinkedIn ? On te le crée de zéro. ✨"
CTA principal : "Analyser mon profil →"
Copyright : © 2026 linktojob.fr — LINK TO JOB
Footer : "Fait avec ❤️ pour tous ceux qui méritent mieux"
```

---

## 🧠 Décisions produit importantes

- **"Open to Work" public = déconseillé** pour tous les profils sauf juniors sans expérience. On conseille toujours "Recruteurs uniquement". Source : Challenges.fr + consensus LinkedIn experts 2026.
- **Création de profil LinkedIn de zéro** = feature V1 différenciante, cible lycéens 16 ans (marché 1)
- **CV + Lettre de motivation** = feature V2, réutiliser le moteur cv-ats-ready existant. Raymond partagera les fichiers au moment du développement.
- **Score freemium** = 3 analyses du même profil (pas 3 URLs différentes). Le vrai produit payant = dashboard de progression dans le temps.
