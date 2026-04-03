"""
stripe_router.py — Intégration Stripe pour Link2Job
- POST /api/stripe/create-checkout  → crée une session de paiement
- POST /api/stripe/webhook          → écoute les événements Stripe
- GET  /api/stripe/success          → confirmation après paiement
"""
import os
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db, User
from auth import require_user

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_ID       = os.getenv("STRIPE_PRICE_ID", "")
FRONTEND_URL          = os.getenv("FRONTEND_URL", "http://127.0.0.1:5500")

router = APIRouter(prefix="/api/stripe", tags=["stripe"])


# ── CRÉER UNE SESSION DE PAIEMENT ────────────────────────────────────

@router.post("/create-checkout")
async def create_checkout(
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """
    Crée une session Stripe Checkout.
    Redirige l'utilisateur vers la page de paiement Stripe.
    """
    if not STRIPE_PRICE_ID:
        raise HTTPException(status_code=500, detail="STRIPE_PRICE_ID non configuré.")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": STRIPE_PRICE_ID,
                "quantity": 1,
            }],
            customer_email=current_user.email,
            metadata={"user_id": str(current_user.id)},
            success_url=f"{FRONTEND_URL}/dashboard.html?upgrade=success",
            cancel_url=f"{FRONTEND_URL}/index.html?upgrade=cancelled",
        )
        return {"checkout_url": session.url, "session_id": session.id}

    except stripe.error.StripeError as e:
        print(f"❌ STRIPE ERROR: {e.user_message} | {e}")
        raise HTTPException(status_code=400, detail=str(e.user_message))


# ── WEBHOOK STRIPE ───────────────────────────────────────────────────

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Reçoit les événements Stripe (paiement réussi, abonnement annulé...).
    Stripe envoie les événements ici automatiquement.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    # Vérifie la signature Stripe (sécurité)
    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        else:
            # En dev sans webhook secret, on parse directement
            import json
            event = json.loads(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    event_type = event.get("type") if isinstance(event, dict) else event.type

    # ── Paiement réussi → upgrade plan ──────────────────────────────
    if event_type == "checkout.session.completed":
        session_data = event["data"]["object"] if isinstance(event, dict) else event.data.object
        user_id = int(session_data.get("metadata", {}).get("user_id", 0))

        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.plan = "candidat"
                db.commit()
                print(f"✅ User {user.email} upgradé vers plan Candidat")

    # ── Abonnement annulé → retour plan free ────────────────────────
    elif event_type in ("customer.subscription.deleted", "customer.subscription.paused"):
        subscription = event["data"]["object"] if isinstance(event, dict) else event.data.object
        customer_email = subscription.get("customer_email") or ""

        if customer_email:
            user = db.query(User).filter(User.email == customer_email).first()
            if user:
                user.plan = "free"
                user.analyses_used = 0  # reset compteur
                db.commit()
                print(f"⚠️ User {user.email} repassé en plan Free")

    return {"status": "ok"}


# ── STATUT ABONNEMENT ────────────────────────────────────────────────

@router.get("/subscription-status")
def subscription_status(current_user: User = Depends(require_user)):
    """Retourne le statut d'abonnement de l'utilisateur."""
    from auth import _analyses_remaining
    return {
        "plan": current_user.plan,
        "analyses_used": current_user.analyses_used,
        "analyses_remaining": _analyses_remaining(current_user),
        "is_premium": current_user.plan != "free",
    }