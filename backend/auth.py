"""
Authentication utilities for JusticiaAI.
Handles JWT token creation/verification and password hashing.
"""
from datetime import datetime, timedelta
from typing import Optional
import re
from jose import JWTError, jwt
import bcrypt
from pydantic import BaseModel, EmailStr, field_validator, Field
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os

from database import get_db
from models import User

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "justiciaai-secret-key-change-in-production-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Bearer token security
security = HTTPBearer()

# Validation constants
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
MAX_NAME_LENGTH = 100


def validate_rut(rut: str) -> bool:
    """
    Valida un RUT chileno.
    Acepta formatos: 12345678-9, 12.345.678-9, 123456789
    """
    # Limpiar el RUT
    rut = rut.upper().replace(".", "").replace("-", "").replace(" ", "")

    if len(rut) < 8 or len(rut) > 9:
        return False

    # Separar cuerpo y dígito verificador
    cuerpo = rut[:-1]
    dv = rut[-1]

    # Validar que el cuerpo sea numérico
    if not cuerpo.isdigit():
        return False

    # Calcular dígito verificador
    suma = 0
    multiplo = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2

    resto = suma % 11
    dv_calculado = 11 - resto

    if dv_calculado == 11:
        dv_esperado = "0"
    elif dv_calculado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_calculado)

    return dv == dv_esperado


def format_rut(rut: str) -> str:
    """Formatea un RUT al formato estándar XX.XXX.XXX-X"""
    rut = rut.upper().replace(".", "").replace("-", "").replace(" ", "")
    if len(rut) < 2:
        return rut
    cuerpo = rut[:-1]
    dv = rut[-1]
    # Formatear con puntos
    cuerpo_formateado = ""
    for i, c in enumerate(reversed(cuerpo)):
        if i > 0 and i % 3 == 0:
            cuerpo_formateado = "." + cuerpo_formateado
        cuerpo_formateado = c + cuerpo_formateado
    return f"{cuerpo_formateado}-{dv}"


def sanitize_string(value: str) -> str:
    """Remove potentially dangerous characters from strings."""
    if not value:
        return value
    # Remove control characters and null bytes
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    # Strip leading/trailing whitespace
    return value.strip()


# Pydantic schemas for auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)
    full_name: Optional[str] = Field(None, max_length=MAX_NAME_LENGTH)
    rut: str = Field(..., min_length=8, max_length=12)
    phone: Optional[str] = Field(None, max_length=20)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < MIN_PASSWORD_LENGTH:
            raise ValueError(f'La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres')
        if len(v) > MAX_PASSWORD_LENGTH:
            raise ValueError(f'La contraseña no puede exceder {MAX_PASSWORD_LENGTH} caracteres')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('La contraseña debe contener al menos una letra')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = sanitize_string(v)
        if len(v) > MAX_NAME_LENGTH:
            raise ValueError(f'El nombre no puede exceder {MAX_NAME_LENGTH} caracteres')
        return v

    @field_validator('rut')
    @classmethod
    def validate_rut_field(cls, v: str) -> str:
        v = sanitize_string(v)
        if not validate_rut(v):
            raise ValueError('RUT inválido. Verifica que esté correcto.')
        return format_rut(v)

    @field_validator('phone')
    @classmethod
    def validate_phone_field(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = sanitize_string(v)
        # Remover caracteres no numéricos excepto +
        cleaned = re.sub(r'[^\d+]', '', v)
        if len(cleaned) < 8 or len(cleaned) > 15:
            raise ValueError('El teléfono debe tener entre 8 y 15 dígitos')
        return cleaned


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=MAX_PASSWORD_LENGTH)


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    rut: Optional[str]
    phone: Optional[str]
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None


class ProfessionalCreate(BaseModel):
    """Schema for professional (lawyer/procurador/estudio) registration."""
    email: EmailStr
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)
    full_name: str = Field(..., min_length=2, max_length=MAX_NAME_LENGTH)
    professional_type: str = Field(..., pattern="^(abogado|procurador|estudio)$")
    specialty: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < MIN_PASSWORD_LENGTH:
            raise ValueError(f'La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres')
        if len(v) > MAX_PASSWORD_LENGTH:
            raise ValueError(f'La contraseña no puede exceder {MAX_PASSWORD_LENGTH} caracteres')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('La contraseña debe contener al menos una letra')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        v = sanitize_string(v)
        if len(v) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        if len(v) > MAX_NAME_LENGTH:
            raise ValueError(f'El nombre no puede exceder {MAX_NAME_LENGTH} caracteres')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v:
            v = sanitize_string(v)
            # Remove non-numeric characters except + for country code
            cleaned = re.sub(r'[^\d+]', '', v)
            if len(cleaned) < 8 or len(cleaned) > 15:
                raise ValueError('El teléfono debe tener entre 8 y 15 dígitos')
            return cleaned
        return v


# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    """Generate a hash for a password."""
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')


# Token utilities
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if email is None:
            return None
        return TokenData(email=email, user_id=user_id)
    except JWTError:
        return None


# User utilities
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by their email address."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate, role: str = "user") -> User:
    """Create a new user in the database."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        rut=user.rut,
        phone=user.phone,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_professional(db: Session, professional: ProfessionalCreate) -> tuple:
    """
    Create a new professional user with their lawyer profile.
    Returns tuple of (User, Lawyer).
    """
    from models import Lawyer, ProfessionalType

    # Create user with lawyer role
    hashed_password = get_password_hash(professional.password)
    db_user = User(
        email=professional.email,
        hashed_password=hashed_password,
        full_name=professional.full_name,
        role="lawyer"  # All professionals have lawyer role for now
    )
    db.add(db_user)
    db.flush()  # Get the user ID without committing

    # Map string to enum
    type_map = {
        "abogado": ProfessionalType.ABOGADO,
        "procurador": ProfessionalType.PROCURADOR,
        "estudio": ProfessionalType.ESTUDIO
    }

    # Create lawyer profile
    db_lawyer = Lawyer(
        user_id=db_user.id,
        name=professional.full_name,
        professional_type=type_map[professional.professional_type],
        specialty=professional.specialty,
        phone=professional.phone,
        is_verified=False
    )
    db.add(db_lawyer)
    db.commit()
    db.refresh(db_user)
    db.refresh(db_lawyer)

    return db_user, db_lawyer


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Dependency to get current user from token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that extracts and verifies the current user from the JWT token.
    Raises HTTPException if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    token_data = decode_token(token)

    if token_data is None:
        raise credentials_exception

    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )

    return user


# Optional dependency - returns None if no token
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional dependency that returns the current user if authenticated,
    or None if no valid token is provided.
    """
    if credentials is None:
        return None

    token_data = decode_token(credentials.credentials)
    if token_data is None:
        return None

    return get_user_by_email(db, email=token_data.email)
