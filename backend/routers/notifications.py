"""
LEIA - Router de Notificaciones

Endpoints para gestionar notificaciones:
- Listar notificaciones
- Marcar como leída
- Contador de no leídas
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import get_db
from auth import get_current_user
from models import User
from models_extended import Notification, NotificationType

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


# ============================================================
# SCHEMAS
# ============================================================

class NotificationResponse(BaseModel):
    """Respuesta de notificación"""
    id: int
    type: NotificationType
    title: str
    description: Optional[str] = None
    related_case_id: Optional[int] = None
    related_transfer_id: Optional[int] = None
    action_url: Optional[str] = None
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Respuesta de lista de notificaciones"""
    notifications: List[NotificationResponse]
    total: int
    unread_count: int
    page: int
    page_size: int


class UnreadCountResponse(BaseModel):
    """Respuesta de contador de no leídas"""
    unread_count: int


# ============================================================
# ENDPOINTS
# ============================================================

@router.get("/", response_model=NotificationListResponse)
async def list_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    unread_only: bool = False,
    notification_type: Optional[NotificationType] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista las notificaciones del usuario actual.

    Soporta:
    - Paginación
    - Filtro por solo no leídas
    - Filtro por tipo de notificación
    """
    query = db.query(Notification).filter(Notification.user_id == current_user.id)

    if unread_only:
        query = query.filter(Notification.is_read == False)

    if notification_type:
        query = query.filter(Notification.type == notification_type)

    # Total count
    total = query.count()

    # Unread count
    unread_count = db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
    ).count()

    # Paginación
    offset = (page - 1) * page_size
    notifications = query.order_by(
        Notification.created_at.desc()
    ).offset(offset).limit(page_size).all()

    return NotificationListResponse(
        notifications=[
            NotificationResponse(
                id=n.id,
                type=n.type,
                title=n.title,
                description=n.description,
                related_case_id=n.related_case_id,
                related_transfer_id=n.related_transfer_id,
                action_url=n.action_url,
                is_read=n.is_read,
                read_at=n.read_at,
                created_at=n.created_at
            )
            for n in notifications
        ],
        total=total,
        unread_count=unread_count,
        page=page,
        page_size=page_size
    )


@router.get("/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el contador de notificaciones no leídas.
    """
    count = db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
    ).count()

    return UnreadCountResponse(unread_count=count)


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marca una notificación como leída.
    """
    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )

    if not notification.is_read:
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        db.commit()

    return {"status": "ok", "message": "Notificación marcada como leída"}


@router.post("/read-all")
async def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marca todas las notificaciones como leídas.
    """
    db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
    ).update({
        "is_read": True,
        "read_at": datetime.utcnow()
    })

    db.commit()

    return {"status": "ok", "message": "Todas las notificaciones marcadas como leídas"}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina una notificación.
    """
    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    ).first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )

    db.delete(notification)
    db.commit()

    return {"status": "ok", "message": "Notificación eliminada"}


@router.delete("/")
async def delete_all_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Elimina todas las notificaciones leídas.
    """
    db.query(Notification).filter(
        and_(
            Notification.user_id == current_user.id,
            Notification.is_read == True
        )
    ).delete()

    db.commit()

    return {"status": "ok", "message": "Notificaciones leídas eliminadas"}
