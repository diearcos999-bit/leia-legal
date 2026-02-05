"""
LEIA - Router de Casos y Transferencias

Endpoints para:
- Crear y gestionar casos
- Transferir casos a abogados
- Gestionar consentimientos
- Timeline de eventos
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from database import get_db
from auth import get_current_user
from models import User, Lawyer, Conversation
from models_extended import (
    Case, CaseTransfer, CaseDocument, CaseEvent, Consent,
    CaseStatus, CasePriority, ConsentType, ServiceType,
    generate_case_number, Notification, NotificationType
)

from models_extended import (
    Case, CaseTransfer, CaseDocument, CaseEvent, Consent, Notification,
    CaseStatus, CasePriority, ConsentType, ServiceType, NotificationType
)

router = APIRouter(prefix="/api/cases", tags=["cases"])


# ============================================================
# SCHEMAS
# ============================================================

class CaseCreate(BaseModel):
    """Crear un nuevo caso"""
    conversation_id: Optional[int] = None
    title: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = None
    legal_area: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None


class CaseSummary(BaseModel):
    """Resumen estructurado del caso generado por IA"""
    facts: List[str] = Field(default_factory=list)
    dates: Dict[str, str] = Field(default_factory=dict)
    legal_area: str
    region: Optional[str] = None
    risk_factors: List[str] = Field(default_factory=list)
    pending_questions: List[str] = Field(default_factory=list)


class CaseUpdate(BaseModel):
    """Actualizar un caso"""
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    legal_area: Optional[str] = None
    sub_area: Optional[str] = None
    priority: Optional[CasePriority] = None
    region: Optional[str] = None
    city: Optional[str] = None
    comuna: Optional[str] = None
    incident_date: Optional[datetime] = None
    deadline_date: Optional[datetime] = None
    risk_level: Optional[int] = Field(None, ge=1, le=10)
    risk_factors: Optional[List[str]] = None
    extracted_facts: Optional[List[str]] = None
    pending_questions: Optional[List[str]] = None


class CaseResponse(BaseModel):
    """Respuesta de caso"""
    id: int
    case_number: str
    title: str
    summary: Optional[str]
    description: Optional[str]
    legal_area: Optional[str]
    sub_area: Optional[str]
    priority: CasePriority
    status: CaseStatus
    region: Optional[str]
    city: Optional[str]
    risk_level: Optional[int]
    risk_factors: Optional[List[str]]
    extracted_facts: Optional[List[str]]
    pending_questions: Optional[List[str]]
    assigned_lawyer_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class TransferRequest(BaseModel):
    """Solicitud de transferencia a abogado"""
    lawyer_id: int
    message: Optional[str] = Field(None, max_length=2000)
    service_type: Optional[ServiceType] = None


class ConsentRequest(BaseModel):
    """Solicitud de consentimiento"""
    consent_types: List[ConsentType]


class ConsentGrant(BaseModel):
    """Otorgar consentimiento"""
    consent_type: ConsentType
    granted: bool


# ============================================================
# ENDPOINTS DE CASOS
# ============================================================

@router.post("/", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: CaseCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo caso.

    El caso inicia en estado DRAFT y puede asociarse a una conversación existente.
    """
    # Verificar que la conversación pertenece al usuario si se proporciona
    if case_data.conversation_id:
        conversation = db.query(Conversation).filter(
            and_(
                Conversation.id == case_data.conversation_id,
                Conversation.user_id == current_user.id
            )
        ).first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversación no encontrada"
            )

    # Generar número de caso
    case_number = generate_case_number(db)

    # Crear caso
    new_case = Case(
        user_id=current_user.id,
        conversation_id=case_data.conversation_id,
        case_number=case_number,
        title=case_data.title,
        description=case_data.description,
        legal_area=case_data.legal_area,
        region=case_data.region,
        city=case_data.city,
        status=CaseStatus.DRAFT,
        priority=CasePriority.MEDIUM
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    # Registrar evento
    event = CaseEvent(
        case_id=new_case.id,
        actor_id=current_user.id,
        event_type="created",
        description=f"Caso {case_number} creado"
    )
    db.add(event)
    db.commit()

    return new_case


@router.get("/", response_model=List[CaseResponse])
async def list_cases(
    status_filter: Optional[CaseStatus] = None,
    legal_area: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista los casos del usuario actual.
    """
    query = db.query(Case).filter(Case.user_id == current_user.id)

    if status_filter:
        query = query.filter(Case.status == status_filter)

    if legal_area:
        query = query.filter(Case.legal_area == legal_area)

    query = query.order_by(Case.created_at.desc())

    # Paginación
    offset = (page - 1) * page_size
    cases = query.offset(offset).limit(page_size).all()

    return cases


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el detalle de un caso.
    """
    case = db.query(Case).filter(
        and_(
            Case.id == case_id,
            Case.user_id == current_user.id
        )
    ).first()

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado"
        )

    return case


@router.put("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: int,
    case_data: CaseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza un caso.
    """
    case = db.query(Case).filter(
        and_(
            Case.id == case_id,
            Case.user_id == current_user.id
        )
    ).first()

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado"
        )

    # Solo se pueden editar casos en DRAFT o READY
    if case.status not in [CaseStatus.DRAFT, CaseStatus.READY_TO_TRANSFER]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede editar un caso ya transferido"
        )

    # Actualizar campos
    update_data = case_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)

    db.commit()
    db.refresh(case)

    return case


@router.post("/{case_id}/summary", response_model=CaseResponse)
async def generate_case_summary(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Genera un resumen estructurado del caso usando IA.

    Analiza la conversación asociada y extrae:
    - Hechos principales
    - Fechas relevantes
    - Área legal
    - Factores de riesgo
    - Preguntas pendientes
    """
    case = db.query(Case).filter(
        and_(
            Case.id == case_id,
            Case.user_id == current_user.id
        )
    ).first()

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado"
        )

    if not case.conversation_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El caso no tiene una conversación asociada"
        )

    # Obtener mensajes de la conversación
    from models import ChatMessage
    messages = db.query(ChatMessage).filter(
        ChatMessage.conversation_id == case.conversation_id
    ).order_by(ChatMessage.created_at).all()

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La conversación no tiene mensajes"
        )

    # Construir el texto de la conversación
    conversation_text = "\n".join([
        f"{'Usuario' if m.role == 'user' else 'LEIA'}: {m.content}"
        for m in messages
    ])

    # Generar resumen con Claude
    import anthropic
    import os

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    summary_prompt = f"""Analiza la siguiente conversación legal y genera un resumen estructurado.

CONVERSACIÓN:
{conversation_text}

Responde SOLO en formato JSON con esta estructura:
{{
    "summary": "Resumen ejecutivo del caso en 2-3 oraciones",
    "facts": ["Hecho 1", "Hecho 2", ...],
    "dates": {{"descripción": "fecha"}},
    "legal_area": "Área legal principal",
    "sub_area": "Sub-área si aplica",
    "risk_level": 1-10,
    "risk_factors": ["Factor 1", "Factor 2", ...],
    "pending_questions": ["Pregunta 1", "Pregunta 2", ...],
    "region": "Región si se menciona",
    "city": "Ciudad si se menciona"
}}

Sé preciso y solo incluye información que esté explícitamente en la conversación."""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{"role": "user", "content": summary_prompt}]
    )

    # Parsear respuesta
    import json
    try:
        summary_data = json.loads(response.content[0].text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al generar el resumen"
        )

    # Actualizar caso
    case.summary = summary_data.get("summary")
    case.extracted_facts = summary_data.get("facts")
    case.extracted_dates = summary_data.get("dates")
    case.legal_area = summary_data.get("legal_area") or case.legal_area
    case.sub_area = summary_data.get("sub_area")
    case.risk_level = summary_data.get("risk_level")
    case.risk_factors = summary_data.get("risk_factors")
    case.pending_questions = summary_data.get("pending_questions")
    case.region = summary_data.get("region") or case.region
    case.city = summary_data.get("city") or case.city
    case.status = CaseStatus.READY_TO_TRANSFER

    db.commit()
    db.refresh(case)

    # Registrar evento
    event = CaseEvent(
        case_id=case.id,
        actor_id=current_user.id,
        event_type="summary_generated",
        description="Resumen del caso generado por IA"
    )
    db.add(event)
    db.commit()

    return case


# ============================================================
# ENDPOINTS DE CONSENTIMIENTO
# ============================================================

@router.post("/{case_id}/consent")
async def grant_consent(
    case_id: int,
    consent_data: ConsentGrant,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Otorga o revoca un consentimiento específico para un caso.
    """
    case = db.query(Case).filter(
        and_(
            Case.id == case_id,
            Case.user_id == current_user.id
        )
    ).first()

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado"
        )

    # Textos de consentimiento
    consent_texts = {
        ConsentType.SHARE_CHAT: "Autorizo compartir el historial completo de mi conversación con LEIA con el abogado seleccionado.",
        ConsentType.SHARE_DOCUMENTS: "Autorizo compartir los documentos adjuntos a mi caso con el abogado seleccionado.",
        ConsentType.SHARE_CONTACT: "Autorizo compartir mis datos de contacto (email, teléfono) con el abogado seleccionado.",
        ConsentType.TRANSFER_CASE: "Autorizo transferir mi caso al abogado seleccionado para que pueda representarme legalmente."
    }

    # Buscar consentimiento existente
    existing = db.query(Consent).filter(
        and_(
            Consent.case_id == case_id,
            Consent.user_id == current_user.id,
            Consent.consent_type == consent_data.consent_type
        )
    ).first()

    if existing:
        existing.granted = consent_data.granted
        if consent_data.granted:
            existing.granted_at = datetime.utcnow()
            existing.revoked_at = None
        else:
            existing.revoked_at = datetime.utcnow()
    else:
        new_consent = Consent(
            user_id=current_user.id,
            case_id=case_id,
            consent_type=consent_data.consent_type,
            granted=consent_data.granted,
            consent_text=consent_texts[consent_data.consent_type],
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            granted_at=datetime.utcnow() if consent_data.granted else None
        )
        db.add(new_consent)

    db.commit()

    # Registrar evento
    event = CaseEvent(
        case_id=case_id,
        actor_id=current_user.id,
        event_type="consent_updated",
        description=f"Consentimiento {'otorgado' if consent_data.granted else 'revocado'}: {consent_data.consent_type.value}",
        event_data={"consent_type": consent_data.consent_type.value, "granted": consent_data.granted}
    )
    db.add(event)
    db.commit()

    return {"status": "ok", "message": f"Consentimiento {'otorgado' if consent_data.granted else 'revocado'}"}


@router.get("/{case_id}/consents")
async def get_case_consents(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el estado de todos los consentimientos de un caso.
    """
    case = db.query(Case).filter(
        and_(
            Case.id == case_id,
            Case.user_id == current_user.id
        )
    ).first()

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado"
        )

    consents = db.query(Consent).filter(
        and_(
            Consent.case_id == case_id,
            Consent.user_id == current_user.id
        )
    ).all()

    # Construir respuesta con todos los tipos
    result = {}
    for consent_type in ConsentType:
        consent = next((c for c in consents if c.consent_type == consent_type), None)
        result[consent_type.value] = {
            "granted": consent.granted if consent else False,
            "granted_at": consent.granted_at.isoformat() if consent and consent.granted_at else None
        }

    return result


# ============================================================
# ENDPOINTS DE TRANSFERENCIA
# ============================================================

@router.post("/{case_id}/transfer")
async def transfer_case(
    case_id: int,
    transfer_data: TransferRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Transfiere un caso a un abogado.

    Requiere:
    1. Que el caso esté en estado READY_TO_TRANSFER
    2. Que el usuario haya dado todos los consentimientos necesarios
    3. Que el abogado exista y esté verificado
    """
    # Verificar caso
    case = db.query(Case).filter(
        and_(
            Case.id == case_id,
            Case.user_id == current_user.id
        )
    ).first()

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado"
        )

    if case.status != CaseStatus.READY_TO_TRANSFER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El caso debe estar listo para transferir. Genera el resumen primero."
        )

    # Verificar consentimientos obligatorios
    required_consents = [ConsentType.SHARE_CHAT, ConsentType.SHARE_CONTACT, ConsentType.TRANSFER_CASE]
    consents = db.query(Consent).filter(
        and_(
            Consent.case_id == case_id,
            Consent.user_id == current_user.id,
            Consent.granted == True
        )
    ).all()

    granted_types = {c.consent_type for c in consents}
    missing = [c.value for c in required_consents if c not in granted_types]

    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Faltan consentimientos: {', '.join(missing)}"
        )

    # Verificar abogado
    lawyer = db.query(Lawyer).filter(
        and_(
            Lawyer.id == transfer_data.lawyer_id,
            Lawyer.is_verified == True
        )
    ).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abogado no encontrado o no verificado"
        )

    # Crear transferencia
    transfer = CaseTransfer(
        case_id=case_id,
        lawyer_id=lawyer.id,
        user_message=transfer_data.message,
        service_type=transfer_data.service_type,
        status="pending"
    )
    db.add(transfer)

    # Actualizar caso
    case.status = CaseStatus.TRANSFERRED
    case.assigned_lawyer_id = lawyer.id
    case.transferred_at = datetime.utcnow()

    db.commit()
    db.refresh(transfer)

    # Registrar evento
    event = CaseEvent(
        case_id=case_id,
        actor_id=current_user.id,
        event_type="transferred",
        description=f"Caso transferido a {lawyer.name}",
        event_data={"lawyer_id": lawyer.id, "transfer_id": transfer.id}
    )
    db.add(event)
    db.commit()

    # TODO: Enviar notificación al abogado

    return {
        "status": "ok",
        "message": f"Caso transferido exitosamente a {lawyer.name}",
        "transfer_id": transfer.id,
        "case_number": case.case_number
    }


@router.get("/{case_id}/transfers")
async def get_case_transfers(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial de transferencias de un caso.
    """
    case = db.query(Case).filter(
        and_(
            Case.id == case_id,
            Case.user_id == current_user.id
        )
    ).first()

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado"
        )

    transfers = db.query(CaseTransfer).filter(
        CaseTransfer.case_id == case_id
    ).order_by(CaseTransfer.created_at.desc()).all()

    return [
        {
            "id": t.id,
            "lawyer_id": t.lawyer_id,
            "status": t.status,
            "user_message": t.user_message,
            "lawyer_response": t.lawyer_response,
            "created_at": t.created_at.isoformat(),
            "accepted_at": t.accepted_at.isoformat() if t.accepted_at else None
        }
        for t in transfers
    ]


# ============================================================
# ENDPOINTS DE TIMELINE
# ============================================================

@router.get("/{case_id}/timeline")
async def get_case_timeline(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el timeline de eventos de un caso.
    """
    case = db.query(Case).filter(
        and_(
            Case.id == case_id,
            Case.user_id == current_user.id
        )
    ).first()

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado"
        )

    events = db.query(CaseEvent).filter(
        CaseEvent.case_id == case_id
    ).order_by(CaseEvent.created_at.desc()).all()

    return [
        {
            "id": e.id,
            "event_type": e.event_type,
            "description": e.description,
            "event_data": e.event_data,
            "created_at": e.created_at.isoformat()
        }
        for e in events
    ]


# ============================================================
# ENDPOINTS PARA ABOGADOS
# ============================================================

class TransferResponseData(BaseModel):
    """Respuesta del abogado a una transferencia"""
    response: str = Field(None, max_length=2000)
    agreed_price: Optional[int] = None


@router.get("/lawyer/pending")
async def get_pending_transfers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene las transferencias pendientes para el abogado actual.
    """
    # Verificar que sea abogado
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los abogados pueden acceder a este endpoint"
        )

    # Obtener transferencias pendientes
    transfers = db.query(CaseTransfer).filter(
        and_(
            CaseTransfer.lawyer_id == lawyer.id,
            CaseTransfer.status == "pending"
        )
    ).order_by(CaseTransfer.created_at.desc()).all()

    result = []
    for t in transfers:
        case = db.query(Case).filter(Case.id == t.case_id).first()
        user = db.query(User).filter(User.id == case.user_id).first() if case else None

        result.append({
            "transfer_id": t.id,
            "case_id": t.case_id,
            "case_number": case.case_number if case else None,
            "case_title": case.title if case else None,
            "case_summary": case.summary if case else None,
            "legal_area": case.legal_area if case else None,
            "priority": case.priority.value if case else None,
            "user_name": user.full_name if user else None,
            "user_message": t.user_message,
            "service_type": t.service_type.value if t.service_type else None,
            "created_at": t.created_at.isoformat()
        })

    return result


@router.get("/lawyer/active")
async def get_active_cases(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene los casos activos del abogado actual.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los abogados pueden acceder a este endpoint"
        )

    # Obtener transferencias aceptadas
    transfers = db.query(CaseTransfer).filter(
        and_(
            CaseTransfer.lawyer_id == lawyer.id,
            CaseTransfer.status == "accepted"
        )
    ).order_by(CaseTransfer.accepted_at.desc()).all()

    result = []
    for t in transfers:
        case = db.query(Case).filter(Case.id == t.case_id).first()
        user = db.query(User).filter(User.id == case.user_id).first() if case else None

        # Contar mensajes no leídos
        from models_extended import CaseMessage
        unread_count = db.query(CaseMessage).filter(
            and_(
                CaseMessage.transfer_id == t.id,
                CaseMessage.sender_type == "user",
                CaseMessage.is_read == False
            )
        ).count()

        # Obtener último mensaje
        last_message = db.query(CaseMessage).filter(
            CaseMessage.transfer_id == t.id
        ).order_by(CaseMessage.created_at.desc()).first()

        result.append({
            "transfer_id": t.id,
            "case_id": t.case_id,
            "case_number": case.case_number if case else None,
            "case_title": case.title if case else None,
            "case_status": case.status.value if case else None,
            "legal_area": case.legal_area if case else None,
            "priority": case.priority.value if case else None,
            "user_name": user.full_name if user else None,
            "accepted_at": t.accepted_at.isoformat() if t.accepted_at else None,
            "unread_messages": unread_count,
            "last_message": {
                "content": last_message.content[:100] if last_message else None,
                "sender_type": last_message.sender_type if last_message else None,
                "created_at": last_message.created_at.isoformat() if last_message else None
            } if last_message else None
        })

    return result


@router.post("/transfers/{transfer_id}/accept")
async def accept_transfer(
    transfer_id: int,
    response_data: TransferResponseData,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Acepta una transferencia de caso.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los abogados pueden aceptar transferencias"
        )

    transfer = db.query(CaseTransfer).filter(
        and_(
            CaseTransfer.id == transfer_id,
            CaseTransfer.lawyer_id == lawyer.id
        )
    ).first()

    if not transfer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transferencia no encontrada"
        )

    if transfer.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La transferencia ya fue procesada"
        )

    # Actualizar transferencia
    transfer.status = "accepted"
    transfer.lawyer_response = response_data.response
    transfer.agreed_price = response_data.agreed_price
    transfer.accepted_at = datetime.utcnow()
    transfer.response_at = datetime.utcnow()

    # Actualizar caso
    case = db.query(Case).filter(Case.id == transfer.case_id).first()
    if case:
        case.status = CaseStatus.IN_PROGRESS

        # Notificar al usuario
        notification = Notification(
            user_id=case.user_id,
            type=NotificationType.CASE_ACCEPTED,
            title="Tu caso fue aceptado",
            description=f"El abogado {lawyer.name} ha aceptado tu caso {case.case_number}",
            related_case_id=case.id,
            related_transfer_id=transfer.id,
            action_url=f"/dashboard/usuario/caso/{case.id}"
        )
        db.add(notification)

        # Registrar evento
        event = CaseEvent(
            case_id=case.id,
            actor_id=current_user.id,
            event_type="transfer_accepted",
            description=f"Abogado {lawyer.name} aceptó el caso",
            event_data={"transfer_id": transfer.id, "agreed_price": response_data.agreed_price}
        )
        db.add(event)

    db.commit()

    return {
        "status": "ok",
        "message": "Transferencia aceptada exitosamente",
        "case_number": case.case_number if case else None
    }


@router.post("/transfers/{transfer_id}/reject")
async def reject_transfer(
    transfer_id: int,
    response_data: TransferResponseData,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rechaza una transferencia de caso.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los abogados pueden rechazar transferencias"
        )

    transfer = db.query(CaseTransfer).filter(
        and_(
            CaseTransfer.id == transfer_id,
            CaseTransfer.lawyer_id == lawyer.id
        )
    ).first()

    if not transfer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transferencia no encontrada"
        )

    if transfer.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La transferencia ya fue procesada"
        )

    # Actualizar transferencia
    transfer.status = "rejected"
    transfer.lawyer_response = response_data.response
    transfer.response_at = datetime.utcnow()

    # Actualizar caso para permitir nueva transferencia
    case = db.query(Case).filter(Case.id == transfer.case_id).first()
    if case:
        case.status = CaseStatus.READY_TO_TRANSFER
        case.assigned_lawyer_id = None

        # Notificar al usuario
        notification = Notification(
            user_id=case.user_id,
            type=NotificationType.CASE_REJECTED,
            title="Tu solicitud fue rechazada",
            description=f"El abogado no pudo aceptar tu caso {case.case_number}. Puedes seleccionar otro abogado.",
            related_case_id=case.id,
            related_transfer_id=transfer.id,
            action_url=f"/dashboard/usuario/caso/{case.id}"
        )
        db.add(notification)

        # Registrar evento
        event = CaseEvent(
            case_id=case.id,
            actor_id=current_user.id,
            event_type="transfer_rejected",
            description=f"Abogado {lawyer.name} rechazó el caso",
            event_data={"transfer_id": transfer.id, "reason": response_data.response}
        )
        db.add(event)

    db.commit()

    return {
        "status": "ok",
        "message": "Transferencia rechazada"
    }


@router.get("/lawyer/case/{case_id}")
async def get_case_for_lawyer(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el detalle de un caso para el abogado asignado.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los abogados pueden acceder a este endpoint"
        )

    # Verificar que el abogado está asignado al caso
    transfer = db.query(CaseTransfer).filter(
        and_(
            CaseTransfer.case_id == case_id,
            CaseTransfer.lawyer_id == lawyer.id,
            CaseTransfer.status.in_(["pending", "accepted"])
        )
    ).first()

    if not transfer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado o no tienes acceso"
        )

    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caso no encontrado"
        )

    user = db.query(User).filter(User.id == case.user_id).first()

    # Obtener historial de chat LEIA si hay consentimiento
    chat_history = []
    consent = db.query(Consent).filter(
        and_(
            Consent.case_id == case_id,
            Consent.consent_type == ConsentType.SHARE_CHAT,
            Consent.granted == True
        )
    ).first()

    if consent and case.conversation_id:
        from models import ChatMessage
        messages = db.query(ChatMessage).filter(
            ChatMessage.conversation_id == case.conversation_id
        ).order_by(ChatMessage.created_at).all()

        chat_history = [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ]

    # Obtener documentos si hay consentimiento
    documents = []
    doc_consent = db.query(Consent).filter(
        and_(
            Consent.case_id == case_id,
            Consent.consent_type == ConsentType.SHARE_DOCUMENTS,
            Consent.granted == True
        )
    ).first()

    if doc_consent:
        docs = db.query(CaseDocument).filter(
            and_(
                CaseDocument.case_id == case_id,
                CaseDocument.shared_with_lawyer == True
            )
        ).all()

        documents = [
            {
                "id": d.id,
                "filename": d.original_filename,
                "file_type": d.file_type,
                "file_size": d.file_size,
                "description": d.description,
                "created_at": d.created_at.isoformat()
            }
            for d in docs
        ]

    # Obtener información de contacto si hay consentimiento
    contact_info = None
    contact_consent = db.query(Consent).filter(
        and_(
            Consent.case_id == case_id,
            Consent.consent_type == ConsentType.SHARE_CONTACT,
            Consent.granted == True
        )
    ).first()

    if contact_consent and user:
        contact_info = {
            "name": user.full_name,
            "email": user.email
        }

    return {
        "case": {
            "id": case.id,
            "case_number": case.case_number,
            "title": case.title,
            "summary": case.summary,
            "description": case.description,
            "legal_area": case.legal_area,
            "sub_area": case.sub_area,
            "priority": case.priority.value,
            "status": case.status.value,
            "region": case.region,
            "city": case.city,
            "risk_level": case.risk_level,
            "risk_factors": case.risk_factors,
            "extracted_facts": case.extracted_facts,
            "pending_questions": case.pending_questions,
            "created_at": case.created_at.isoformat()
        },
        "transfer": {
            "id": transfer.id,
            "status": transfer.status,
            "user_message": transfer.user_message,
            "agreed_price": transfer.agreed_price,
            "service_type": transfer.service_type.value if transfer.service_type else None,
            "created_at": transfer.created_at.isoformat(),
            "accepted_at": transfer.accepted_at.isoformat() if transfer.accepted_at else None
        },
        "contact_info": contact_info,
        "chat_history": chat_history,
        "documents": documents
    }
