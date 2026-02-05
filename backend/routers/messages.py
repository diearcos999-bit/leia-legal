"""
LEIA - Router de Mensajes

Endpoints para la comunicación entre usuarios y abogados:
- Enviar mensajes
- Obtener historial de mensajes
- Marcar como leído
- Contador de no leídos
"""

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import os
import uuid

from database import get_db
from auth import get_current_user
from models import User, Lawyer
from models_extended import (
    Case, CaseTransfer, CaseMessage, Notification,
    MessageType, NotificationType, CaseStatus
)

router = APIRouter(prefix="/api/messages", tags=["messages"])


# ============================================================
# SCHEMAS
# ============================================================

class MessageCreate(BaseModel):
    """Crear un nuevo mensaje"""
    content: str = Field(..., min_length=1, max_length=5000)
    message_type: MessageType = MessageType.TEXT


class MessageResponse(BaseModel):
    """Respuesta de mensaje"""
    id: int
    transfer_id: int
    sender_id: int
    sender_type: str
    sender_name: Optional[str] = None
    content: str
    message_type: MessageType
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UnreadCountResponse(BaseModel):
    """Respuesta de contador de no leídos"""
    total_unread: int
    by_transfer: dict


# ============================================================
# HELPERS
# ============================================================

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


def create_notification(
    db: Session,
    user_id: int,
    notification_type: NotificationType,
    title: str,
    description: str = None,
    related_case_id: int = None,
    related_transfer_id: int = None,
    action_url: str = None
):
    """Crea una notificación para un usuario."""
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        description=description,
        related_case_id=related_case_id,
        related_transfer_id=related_transfer_id,
        action_url=action_url
    )
    db.add(notification)
    return notification


# ============================================================
# ENDPOINTS
# ============================================================

@router.post("/transfers/{transfer_id}/messages", response_model=MessageResponse)
async def send_message(
    transfer_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Envía un mensaje en una conversación de caso.

    Solo usuarios y abogados involucrados en el caso pueden enviar mensajes.
    La transferencia debe estar en estado 'accepted' para permitir mensajes.
    """
    transfer, sender_type = get_user_transfer_access(transfer_id, current_user, db)

    # Verificar que la transferencia esté aceptada
    if transfer.status not in ["accepted", "pending"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La transferencia debe estar activa para enviar mensajes"
        )

    # Crear mensaje
    message = CaseMessage(
        transfer_id=transfer_id,
        sender_id=current_user.id,
        sender_type=sender_type,
        content=message_data.content,
        message_type=message_data.message_type
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    # Crear notificación para el destinatario
    case = db.query(Case).filter(Case.id == transfer.case_id).first()

    if sender_type == "user":
        # Notificar al abogado
        lawyer = db.query(Lawyer).filter(Lawyer.id == transfer.lawyer_id).first()
        if lawyer and lawyer.user_id:
            create_notification(
                db=db,
                user_id=lawyer.user_id,
                notification_type=NotificationType.NEW_MESSAGE,
                title="Nuevo mensaje de cliente",
                description=f"Tienes un nuevo mensaje en el caso {case.case_number}",
                related_case_id=case.id,
                related_transfer_id=transfer_id,
                action_url=f"/dashboard/profesional/caso/{case.id}"
            )
    else:
        # Notificar al usuario
        create_notification(
            db=db,
            user_id=case.user_id,
            notification_type=NotificationType.NEW_MESSAGE,
            title="Nuevo mensaje de tu abogado",
            description=f"Tu abogado ha enviado un mensaje en tu caso {case.case_number}",
            related_case_id=case.id,
            related_transfer_id=transfer_id,
            action_url=f"/dashboard/usuario/caso/{case.id}"
        )

    db.commit()

    # Obtener nombre del sender
    sender_name = current_user.full_name or current_user.email

    return MessageResponse(
        id=message.id,
        transfer_id=message.transfer_id,
        sender_id=message.sender_id,
        sender_type=message.sender_type,
        sender_name=sender_name,
        content=message.content,
        message_type=message.message_type,
        file_path=message.file_path,
        file_name=message.file_name,
        file_size=message.file_size,
        is_read=message.is_read,
        read_at=message.read_at,
        created_at=message.created_at
    )


@router.get("/transfers/{transfer_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    transfer_id: int,
    limit: int = 50,
    before_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial de mensajes de una conversación.

    Soporta paginación con before_id para cargar mensajes más antiguos.
    """
    transfer, participant_type = get_user_transfer_access(transfer_id, current_user, db)

    # Query de mensajes
    query = db.query(CaseMessage).filter(CaseMessage.transfer_id == transfer_id)

    if before_id:
        query = query.filter(CaseMessage.id < before_id)

    messages = query.order_by(CaseMessage.created_at.desc()).limit(limit).all()

    # Obtener información de los senders
    user_ids = list(set(m.sender_id for m in messages))
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    user_map = {u.id: u.full_name or u.email for u in users}

    # Invertir para orden cronológico
    messages.reverse()

    return [
        MessageResponse(
            id=m.id,
            transfer_id=m.transfer_id,
            sender_id=m.sender_id,
            sender_type=m.sender_type,
            sender_name=user_map.get(m.sender_id),
            content=m.content,
            message_type=m.message_type,
            file_path=m.file_path,
            file_name=m.file_name,
            file_size=m.file_size,
            is_read=m.is_read,
            read_at=m.read_at,
            created_at=m.created_at
        )
        for m in messages
    ]


@router.post("/transfers/{transfer_id}/messages/read")
async def mark_messages_read(
    transfer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marca todos los mensajes no leídos de una conversación como leídos.

    Solo marca como leídos los mensajes del otro participante.
    """
    transfer, participant_type = get_user_transfer_access(transfer_id, current_user, db)

    # Determinar el tipo de sender a marcar (el opuesto al actual)
    other_type = "lawyer" if participant_type == "user" else "user"

    # Actualizar mensajes no leídos
    db.query(CaseMessage).filter(
        and_(
            CaseMessage.transfer_id == transfer_id,
            CaseMessage.sender_type == other_type,
            CaseMessage.is_read == False
        )
    ).update({
        "is_read": True,
        "read_at": datetime.utcnow()
    })

    db.commit()

    return {"status": "ok", "message": "Mensajes marcados como leídos"}


@router.get("/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el contador de mensajes no leídos para el usuario actual.

    Retorna el total y desglosado por transferencia.
    """
    # Determinar el tipo de participante del usuario
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if lawyer:
        # Es abogado - buscar mensajes de usuarios en sus transferencias
        transfers = db.query(CaseTransfer).filter(
            CaseTransfer.lawyer_id == lawyer.id
        ).all()
        transfer_ids = [t.id for t in transfers]
        sender_type_to_count = "user"
    else:
        # Es usuario - buscar mensajes de abogados en sus casos
        cases = db.query(Case).filter(Case.user_id == current_user.id).all()
        case_ids = [c.id for c in cases]
        transfers = db.query(CaseTransfer).filter(
            CaseTransfer.case_id.in_(case_ids)
        ).all()
        transfer_ids = [t.id for t in transfers]
        sender_type_to_count = "lawyer"

    if not transfer_ids:
        return UnreadCountResponse(total_unread=0, by_transfer={})

    # Contar mensajes no leídos
    unread_counts = db.query(
        CaseMessage.transfer_id,
        func.count(CaseMessage.id).label("count")
    ).filter(
        and_(
            CaseMessage.transfer_id.in_(transfer_ids),
            CaseMessage.sender_type == sender_type_to_count,
            CaseMessage.is_read == False
        )
    ).group_by(CaseMessage.transfer_id).all()

    by_transfer = {str(t_id): count for t_id, count in unread_counts}
    total = sum(count for _, count in unread_counts)

    return UnreadCountResponse(total_unread=total, by_transfer=by_transfer)


@router.post("/transfers/{transfer_id}/messages/file", response_model=MessageResponse)
async def send_file_message(
    transfer_id: int,
    file: UploadFile = File(...),
    message: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Envía un mensaje con archivo adjunto.

    Tipos permitidos: PDF, imágenes, documentos de Office.
    Tamaño máximo: 10MB.
    """
    transfer, sender_type = get_user_transfer_access(transfer_id, current_user, db)

    # Verificar que la transferencia esté aceptada
    if transfer.status not in ["accepted", "pending"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La transferencia debe estar activa para enviar archivos"
        )

    # Validar tipo de archivo
    allowed_types = [
        "application/pdf",
        "image/jpeg", "image/png", "image/gif",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de archivo no permitido"
        )

    # Validar tamaño (10MB)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo excede el tamaño máximo de 10MB"
        )

    # Guardar archivo
    case = db.query(Case).filter(Case.id == transfer.case_id).first()
    upload_dir = f"uploads/cases/{case.id}"
    os.makedirs(upload_dir, exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = f"{upload_dir}/{unique_filename}"

    with open(file_path, "wb") as f:
        f.write(contents)

    # Crear mensaje
    case_message = CaseMessage(
        transfer_id=transfer_id,
        sender_id=current_user.id,
        sender_type=sender_type,
        content=message or f"Archivo adjunto: {file.filename}",
        message_type=MessageType.FILE,
        file_path=file_path,
        file_name=file.filename,
        file_size=len(contents)
    )

    db.add(case_message)
    db.commit()
    db.refresh(case_message)

    sender_name = current_user.full_name or current_user.email

    return MessageResponse(
        id=case_message.id,
        transfer_id=case_message.transfer_id,
        sender_id=case_message.sender_id,
        sender_type=case_message.sender_type,
        sender_name=sender_name,
        content=case_message.content,
        message_type=case_message.message_type,
        file_path=case_message.file_path,
        file_name=case_message.file_name,
        file_size=case_message.file_size,
        is_read=case_message.is_read,
        read_at=case_message.read_at,
        created_at=case_message.created_at
    )
