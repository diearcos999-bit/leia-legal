"""
OAuth Authentication Router for LEIA.
Handles Google, Facebook, LinkedIn, and Apple OAuth.
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
import httpx
import os
import secrets

from database import get_db
from models import User
from auth import (
    create_access_token, get_user_by_email, get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES, UserResponse
)

router = APIRouter(prefix="/api/auth/oauth", tags=["oauth"])

# OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


@router.get("/google")
async def google_login():
    """
    Redirect to Google OAuth login page.
    """
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=503,
            detail="Google OAuth no está configurado. Usa registro con email."
        )

    redirect_uri = f"{BACKEND_URL}/api/auth/oauth/google/callback"
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={redirect_uri}&"
        "response_type=code&"
        "scope=openid%20email%20profile&"
        "access_type=offline"
    )
    return RedirectResponse(url=google_auth_url)


@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    """
    Handle Google OAuth callback.
    """
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=503, detail="Google OAuth no configurado")

    redirect_uri = f"{BACKEND_URL}/api/auth/oauth/google/callback"

    # Exchange code for tokens
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Error al obtener token de Google")

        tokens = token_response.json()
        access_token = tokens.get("access_token")

        # Get user info
        user_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Error al obtener información del usuario")

        user_info = user_response.json()

    email = user_info.get("email")
    name = user_info.get("name", "")

    if not email:
        raise HTTPException(status_code=400, detail="No se pudo obtener el email de Google")

    # Check if user exists
    user = get_user_by_email(db, email)

    if not user:
        # Create new user
        random_password = secrets.token_urlsafe(32)
        user = User(
            email=email,
            hashed_password=get_password_hash(random_password),
            full_name=name,
            is_verified=True,  # Google verified the email
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create JWT token
    jwt_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Redirect to frontend with token
    redirect_url = f"{FRONTEND_URL}/auth/callback?token={jwt_token}&user={user.email}"
    return RedirectResponse(url=redirect_url)


@router.get("/facebook")
async def facebook_login():
    """Redirect to Facebook OAuth - placeholder."""
    raise HTTPException(
        status_code=503,
        detail="Facebook OAuth próximamente. Usa Google o registro con email."
    )


@router.get("/linkedin")
async def linkedin_login():
    """Redirect to LinkedIn OAuth - placeholder."""
    raise HTTPException(
        status_code=503,
        detail="LinkedIn OAuth próximamente. Usa Google o registro con email."
    )


@router.get("/apple")
async def apple_login():
    """Redirect to Apple OAuth - placeholder."""
    raise HTTPException(
        status_code=503,
        detail="Apple OAuth próximamente. Usa Google o registro con email."
    )
