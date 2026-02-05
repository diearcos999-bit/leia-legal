"""
Authentication router for LEIA.
Handles user registration, login, and profile management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta

from database import get_db
from models import User, Lawyer
from auth import (
    UserCreate, UserLogin, UserResponse, Token, ProfessionalCreate,
    authenticate_user, create_user, create_professional, get_user_by_email,
    create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario.
    """
    # Check if user exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Create user
    user = create_user(db, user_data)

    # Create token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/register/professional")
async def register_professional(professional_data: ProfessionalCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo profesional (abogado, procurador o estudio).
    """
    # Check if user exists
    existing_user = get_user_by_email(db, professional_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Create professional
    user, lawyer = create_professional(db, professional_data)

    # Create token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
        "lawyer_id": lawyer.id
    }


@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Inicia sesión y devuelve un token JWT.
    """
    user = authenticate_user(db, credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user has a lawyer profile
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == user.id).first()

    # Create token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
        "lawyer_id": lawyer.id if lawyer else None
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Retorna la información del usuario autenticado actual.
    """
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    full_name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza la información del usuario autenticado.
    """
    if full_name:
        current_user.full_name = full_name
        db.commit()
        db.refresh(current_user)

    return UserResponse.model_validate(current_user)
