"""
stripe_router.py — Intégration Stripe pour Link2Job
"""
import os
import re
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db, User
from auth import require_user

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_ID       = os.getenv("STRIPE_PRICE_ID", "")

router = APIRouter(prefix="/api/stripe", tags=["stripe"])


def sanitize(s: str) -> str:
    """Supprime tout caractère non-ASCII pour éviter UnicodeEncodeError avec Stripe."""
    if not s:
        return ""
    # Garde uniquement les caractères ASCII imprimables
    return re.sub(r'[^\x20-\x7E]', '', str(s))


# ── CRÉER UNE SESSION DE PAIEMENT ────────────────────────────────────

@router.post("/create-checkout")
async def create_checkout(
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    if not STRIPE_PRICE_ID:
        raise HTTPException(status_code=500, detail="STRIPE_PRICE_ID non configuré.")

    # Sanitise toutes les données avant envoi à Stripe
    safe_email   = sanitize(current_user.email)
    safe_user_id = sanitize(str(current_user.id))

    print(f"[Stripe] Checkout pour user_id={safe_user_id} email={safe_email}")
    print(f"[Stripe] PRICE_ID={STRIPE_PRICE_ID}")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": STRIPE_PRICE_ID,
                "quantity": 1,
            }],
            customer_email=safe_email,
            metadata={"user_id": safe_user_id},
            success_url="http://localhost:5500/dashboard.html?upgrade=success",
            cancel_url="http://localhost:5500/index.html?upgrade=cancelled",
        )
        print(f"[Stripe] Session créée : {session.id}")
        return {"checkout_url": session.url, "session_id": session.id}

    except stripe.error.StripeError as e:
        print(f"[Stripe] ERREUR : {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[Stripe] ERREUR INATTENDUE : {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── WEBHOOK STRIPE ───────────────────────────────────────────────────

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload    = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        else:
            import json
            event = json.loads(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    event_type = event.get("type") if isinstance(event, dict) else event.type

    if event_type == "checkout.session.completed":
            session_data = event["data"]["object"] if isinstance(event, dict) else event.data.object
            # Objet Stripe → accès par attribut, pas par .get()
            try:
                metadata = session_data.metadata if hasattr(session_data, 'metadata') else session_data.get("metadata", {})
                user_id = int(metadata.get("user_id", 0) if isinstance(metadata, dict) else metadata["user_id"])
            except Exception:
                user_id = 0
            if user_id:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    user.plan = "candidat"
                    db.commit()
                    print(f"[Stripe] ✅ User {user.email} upgradé vers plan Candidat")

    elif event_type in ("customer.subscription.deleted", "customer.subscription.paused"):
            session_data = event["data"]["object"] if isinstance(event, dict) else event.data.object
            try:
                customer_email = session_data.customer_email if hasattr(session_data, 'customer_email') else session_data.get("customer_email", "")
            except Exception:
                customer_email = ""


# ── STATUT ABONNEMENT ────────────────────────────────────────────────

@router.get("/subscription-status")
def subscription_status(current_user: User = Depends(require_user)):
    from auth import _analyses_remaining
    return {
        "plan": current_user.plan,
        "analyses_used": current_user.analyses_used,
        "analyses_remaining": _analyses_remaining(current_user),
        "is_premium": current_user.plan != "free",
    }