async def parse_linkedin_profile(url: str) -> dict | None:
    """MODE DEV — profil mocké pour tester le pipeline complet."""
    return {
        "url": url,
        "name": "Raymond Gadji",
        "headline": "Étudiant en Data Science",
        "about": "",
        "location": "Paris, France",
        "connections": "67",
        "experiences": ["Stage Data Analyst — Startup Paris"],
        "education": ["EmLyon Business School"],
        "skills": ["Python", "SQL", "Excel"],
        "recommendations_count": 0,
        "certifications": [],
        "has_photo": True,
        "has_activity": False,
    }