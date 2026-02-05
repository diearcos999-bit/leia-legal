"""
LEIA - Router de Llamadas

Endpoints para llamadas de voz y video usando Daily.co:
- Solicitar llamada
- Aceptar/Rechazar llamada
- Terminar llamada
- Obtener token de sala
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os
import httpx
import uuid

from database import get_db
from auth import get_current_user
from models import User, Lawyer
from models_extended import (
    Case, CaseTransfer, CallSession, Notification,
    LawyerCommunicationSettings,
    CallType, CallStatus, NotificationType
)

router = APIRouter(prefix="/api/calls", tags=["calls"])

# Daily.co configuration
DAILY_API_KEY = os.getenv("DAILY_API_KEY")
DAILY_API_URL = "https://api.daily.co/v1"


# ============================================================
# SCHEMAS
# ============================================================

class CallRequest(BaseModel):
    """Solicitud de llamada"""
    call_type: CallType


class CallResponse(BaseModel):
    """Respuesta de llamada"""
    id: int
    transfer_id: int
    call_type: CallType
    status: CallStatus
    room_url: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RoomTokenResponse(BaseModel):
    """Token para unirse a sala"""
    room_url: str
    token: str
    expires_at: datetime


# ============================================================
# HELPERS
# ============================================================

async def create_daily_room(room_name: str) -> dict:
    """Crea una sala en Daily.co."""
    if not DAILY_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio de llamadas no configurado"
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DAILY_API_URL}/rooms",
            headers={"Authorization": f"Bearer {DAILY_API_KEY}"},
            json={
                "name": room_name,
                "privacy": "private",
                "properties": {
                    "max_participants": 2,
                    "enable_chat": True,
                    "enable_screenshare": False,
                    "exp": int((datetime.utcnow().timestamp()) + 3600)  # 1 hour expiry
                }
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Error al crear sala de llamada"
            )

        return response.json()


async def create_daily_token(room_name: str, user_name: str, is_owner: bool = False) -> dict:
    """Crea un token de acceso para una sala de Daily.co."""
    if not DAILY_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio de llamadas no configurado"
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DAILY_API_URL}/meeting-tokens",
            headers={"Authorization": f"Bearer {DAILY_API_KEY}"},
            json={
                "properties": {
                    "room_name": room_name,
                    "user_name": user_name,
                    "is_owner": is_owner,
                    "exp": int((datetime.utcnow().timestamp()) + 3600)  # 1 hour
                }
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Error al crear token de acceso"
            )

        return response.json()


async def delete_daily_room(room_name: str):
    """Elimina una sala de Daily.co."""
    if not DAILY_API_KEY:
        return

    async with httpx.AsyncClient() as client:
        await client.delete(
            f"{DAILY_API_URL}/rooms/{room_name}",
            headers={"Authorization": f"Bearer {DAILY_API_KEY}"}
        )


def get_user_transfer_access(
    transfer_id: int,
    current_user: User,
    db: Session
) -> tuple[CaseTransfer, str]:
    """
    Verifica que el usuario tenga acceso a la transferencia.
    Retorna la transferencia y el tipo de participante ('user' o 'lawyer').
    """
    transfer = db.query(CaseTransfer).filter(CaseTransfer.id == transfer_id).first()

    if not transfer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transferencia no encontrada"
        )

    # Verificar si es el usuario del caso
    case = db.query(Case).filter(Case.id == transfer.case_id).first()
    if case and case.user_id == current_user.id:
        return transfer, "user"

    # Verificar si es el abogado asignado
    lawyer = db.query(Lawyer).filter(
        and_(
            Lawyer.id == transfer.lawyer_id,
            Lawyer.user_id == current_user.id
        )
    ).first()

    if lawyer:
        return transfer, "lawyer"

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes acceso a esta conversación"
    )


# ============================================================
# ENDPOINTS
# ============================================================

@router.post("/transfers/{transfer_id}/request", response_model=CallResponse)
async def request_call(
    transfer_id: int,
    call_data: CallRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Solicita una llamada con el otro participante.

    Verifica que el abogado tenga habilitado el tipo de llamada solicitado.
    """
    transfer, participant_type = get_user_transfer_access(transfer_id, current_user, db)

    # Verificar que la transferencia esté aceptada
    if transfer.status != "accepted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La transferencia debe estar aceptada para iniciar llamadas"
        )

    # Verificar configuración de comunicación del abogado
    settings = db.query(LawyerCommunicationSettings).filter(
        LawyerCommunicationSettings.lawyer_id == transfer.lawyer_id
    ).first()

    if not settings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El abogado no tiene configurada la comunicación"
        )

    if call_data.call_type == CallType.VOICE and not settings.voice_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El abogado no tiene habilitadas las llamadas de voz"
        )

    if call_data.call_type == CallType.VIDEO and not settings.video_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El abogado no tiene habilitadas las videollamadas"
        )

    # Verificar que no haya una llamada activa
    active_call = db.query(CallSession).filter(
        and_(
            CallSession.transfer_id == transfer_id,
            CallSession.status.in_([CallStatus.PENDING, CallStatus.RINGING, CallStatus.IN_PROGRESS])
        )
    ).first()

    if active_call:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya hay una llamada activa en esta conversación"
        )

    # Crear sala en Daily.co
    room_name = f"leia-{transfer_id}-{uuid.uuid4().hex[:8]}"

    try:
        room_data = await create_daily_room(room_name)
        room_url = room_data.get("url")
    except Exception:
        # Si no hay Daily.co configurado, crear llamada sin sala
        room_url = None
        room_name = None

    # Crear sesión de llamada
    call_session = CallSession(
        transfer_id=transfer_id,
        initiated_by=current_user.id,
        call_type=call_data.call_type,
        status=CallStatus.RINGING,
        room_id=room_name,
        room_url=room_url
    )

    db.add(call_session)
    db.commit()
    db.refresh(call_session)

    # Notificar al otro participante
    case = db.query(Case).filter(Case.id == transfer.case_id).first()

    if participant_type == "user":
        # Notificar al abogado
        lawyer = db.query(Lawyer).filter(Lawyer.id == transfer.lawyer_id).first()
        if lawyer and lawyer.user_id:
            notification = Notification(
                user_id=lawyer.user_id,
                type=NotificationType.CALL_REQUEST,
                title=f"Llamada entrante - {call_data.call_type.value}",
                description=f"El cliente del caso {case.case_number} está llamando",
                related_case_id=case.id,
                related_transfer_id=transfer_id,
                action_url=f"/dashboard/profesional/caso/{case.id}?call={call_session.id}"
            )
            db.add(notification)
    else:
        # Notificar al usuario
        notification = Notification(
            user_id=case.user_id,
            type=NotificationType.CALL_REQUEST,
            title=f"Llamada entrante - {call_data.call_type.value}",
            description=f"Tu abogado está llamando",
            related_case_id=case.id,
            related_transfer_id=transfer_id,
            action_url=f"/dashboard/usuario/caso/{case.id}?call={call_session.id}"
        )
        db.add(notification)

    db.commit()

    return CallResponse(
        id=call_session.id,
        transfer_id=call_session.transfer_id,
        call_type=call_session.call_type,
        status=call_session.status,
        room_url=call_session.room_url,
        started_at=call_session.started_at,
        ended_at=call_session.ended_at,
        duration_seconds=call_session.duration_seconds,
        created_at=call_session.created_at
    )


@router.post("/{call_id}/accept", response_model=CallResponse)
async def accept_call(
    call_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Acepta una llamada entrante.
    """
    call_session = db.query(CallSession).filter(CallSession.id == call_id).first()

    if not call_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Llamada no encontrada"
        )

    # Verificar acceso
    transfer, _ = get_user_transfer_access(call_session.transfer_id, current_user, db)

    # Verificar que no sea quien inició la llamada
    if call_session.initiated_by == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes aceptar tu propia llamada"
        )

    # Verificar estado
    if call_session.status != CallStatus.RINGING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La llamada no está en estado de espera"
        )

    # Actualizar estado
    call_session.status = CallStatus.IN_PROGRESS
    call_session.started_at = datetime.utcnow()
    db.commit()
    db.refresh(call_session)

    return CallResponse(
        id=call_session.id,
        transfer_id=call_session.transfer_id,
        call_type=call_session.call_type,
        status=call_session.status,
        room_url=call_session.room_url,
        started_at=call_session.started_at,
        ended_at=call_session.ended_at,
        duration_seconds=call_session.duration_seconds,
        created_at=call_session.created_at
    )


@router.post("/{call_id}/reject", response_model=CallResponse)
async def reject_call(
    call_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rechaza una llamada entrante.
    """
    call_session = db.query(CallSession).filter(CallSession.id == call_id).first()

    if not call_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Llamada no encontrada"
        )

    # Verificar acceso
    transfer, participant_type = get_user_transfer_access(call_session.transfer_id, current_user, db)

    # Verificar estado
    if call_session.status not in [CallStatus.PENDING, CallStatus.RINGING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La llamada no puede ser rechazada"
        )

    # Actualizar estado
    call_session.status = CallStatus.REJECTED
    call_session.ended_at = datetime.utcnow()
    db.commit()

    # Eliminar sala si existe
    if call_session.room_id:
        await delete_daily_room(call_session.room_id)

    # Notificar llamada perdida
    case = db.query(Case).filter(Case.id == transfer.case_id).first()

    notification = Notification(
        user_id=call_session.initiated_by,
        type=NotificationType.CALL_MISSED,
        title="Llamada rechazada",
        description=f"Tu llamada en el caso {case.case_number} fue rechazada",
        related_case_id=case.id,
        related_transfer_id=transfer.id
    )
    db.add(notification)
    db.commit()
    db.refresh(call_session)

    return CallResponse(
        id=call_session.id,
        transfer_id=call_session.transfer_id,
        call_type=call_session.call_type,
        status=call_session.status,
        room_url=call_session.room_url,
        started_at=call_session.started_at,
        ended_at=call_session.ended_at,
        duration_seconds=call_session.duration_seconds,
        created_at=call_session.created_at
    )


@router.post("/{call_id}/end", response_model=CallResponse)
async def end_call(
    call_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Termina una llamada en progreso.
    """
    call_session = db.query(CallSession).filter(CallSession.id == call_id).first()

    if not call_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Llamada no encontrada"
        )

    # Verificar acceso
    get_user_transfer_access(call_session.transfer_id, current_user, db)

    # Verificar estado
    if call_session.status not in [CallStatus.IN_PROGRESS, CallStatus.RINGING, CallStatus.PENDING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La llamada no está activa"
        )

    # Calcular duración
    if call_session.started_at:
        duration = (datetime.utcnow() - call_session.started_at).total_seconds()
        call_session.duration_seconds = int(duration)
        call_session.status = CallStatus.COMPLETED
    else:
        call_session.status = CallStatus.MISSED

    call_session.ended_at = datetime.utcnow()
    db.commit()

    # Eliminar sala
    if call_session.room_id:
        await delete_daily_room(call_session.room_id)

    db.refresh(call_session)

    return CallResponse(
        id=call_session.id,
        transfer_id=call_session.transfer_id,
        call_type=call_session.call_type,
        status=call_session.status,
        room_url=call_session.room_url,
        started_at=call_session.started_at,
        ended_at=call_session.ended_at,
        duration_seconds=call_session.duration_seconds,
        created_at=call_session.created_at
    )


@router.get("/{call_id}/token", response_model=RoomTokenResponse)
async def get_call_token(
    call_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el token para unirse a la sala de llamada.
    """
    call_session = db.query(CallSession).filter(CallSession.id == call_id).first()

    if not call_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Llamada no encontrada"
        )

    # Verificar acceso
    get_user_transfer_access(call_session.transfer_id, current_user, db)

    # Verificar estado
    if call_session.status not in [CallStatus.RINGING, CallStatus.IN_PROGRESS]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La llamada no está activa"
        )

    if not call_session.room_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sala de llamada no disponible"
        )

    # Crear token
    user_name = current_user.full_name or current_user.email
    is_owner = call_session.initiated_by == current_user.id

    token_data = await create_daily_token(call_session.room_id, user_name, is_owner)

    return RoomTokenResponse(
        room_url=call_session.room_url,
        token=token_data.get("token"),
        expires_at=datetime.utcnow().replace(hour=datetime.utcnow().hour + 1)
    )


@router.get("/transfers/{transfer_id}/active", response_model=Optional[CallResponse])
async def get_active_call(
    transfer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la llamada activa de una transferencia (si existe).
    """
    get_user_transfer_access(transfer_id, current_user, db)

    active_call = db.query(CallSession).filter(
        and_(
            CallSession.transfer_id == transfer_id,
            CallSession.status.in_([CallStatus.PENDING, CallStatus.RINGING, CallStatus.IN_PROGRESS])
        )
    ).first()

    if not active_call:
        return None

    return CallResponse(
        id=active_call.id,
        transfer_id=active_call.transfer_id,
        call_type=active_call.call_type,
        status=active_call.status,
        room_url=active_call.room_url,
        started_at=active_call.started_at,
        ended_at=active_call.ended_at,
        duration_seconds=active_call.duration_seconds,
        created_at=active_call.created_at
    )


# ============================================================
# LAWYER COMMUNICATION SETTINGS
# ============================================================

class CommunicationSettingsUpdate(BaseModel):
    """Actualización de configuración de comunicación"""
    chat_enabled: Optional[bool] = None
    voice_enabled: Optional[bool] = None
    video_enabled: Optional[bool] = None
    available_hours: Optional[dict] = None
    response_time_target: Optional[int] = None
    is_available: Optional[bool] = None
    unavailable_until: Optional[datetime] = None
    unavailable_message: Optional[str] = None


class CommunicationSettingsResponse(BaseModel):
    """Respuesta de configuración de comunicación"""
    chat_enabled: bool
    voice_enabled: bool
    video_enabled: bool
    available_hours: Optional[dict] = None
    response_time_target: int
    is_available: bool
    unavailable_until: Optional[datetime] = None
    unavailable_message: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/settings", response_model=CommunicationSettingsResponse)
async def get_communication_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la configuración de comunicación del abogado actual.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los abogados pueden acceder a esta configuración"
        )

    settings = db.query(LawyerCommunicationSettings).filter(
        LawyerCommunicationSettings.lawyer_id == lawyer.id
    ).first()

    if not settings:
        # Crear configuración por defecto
        settings = LawyerCommunicationSettings(
            lawyer_id=lawyer.id,
            chat_enabled=True,
            voice_enabled=False,
            video_enabled=False,
            response_time_target=24
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return CommunicationSettingsResponse(
        chat_enabled=settings.chat_enabled,
        voice_enabled=settings.voice_enabled,
        video_enabled=settings.video_enabled,
        available_hours=settings.available_hours,
        response_time_target=settings.response_time_target,
        is_available=settings.is_available,
        unavailable_until=settings.unavailable_until,
        unavailable_message=settings.unavailable_message
    )


@router.put("/settings", response_model=CommunicationSettingsResponse)
async def update_communication_settings(
    settings_data: CommunicationSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza la configuración de comunicación del abogado.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los abogados pueden modificar esta configuración"
        )

    settings = db.query(LawyerCommunicationSettings).filter(
        LawyerCommunicationSettings.lawyer_id == lawyer.id
    ).first()

    if not settings:
        settings = LawyerCommunicationSettings(lawyer_id=lawyer.id)
        db.add(settings)

    # Actualizar campos
    update_data = settings_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)

    db.commit()
    db.refresh(settings)

    return CommunicationSettingsResponse(
        chat_enabled=settings.chat_enabled,
        voice_enabled=settings.voice_enabled,
        video_enabled=settings.video_enabled,
        available_hours=settings.available_hours,
        response_time_target=settings.response_time_target,
        is_available=settings.is_available,
        unavailable_until=settings.unavailable_until,
        unavailable_message=settings.unavailable_message
    )
