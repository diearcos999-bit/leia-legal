"""
LEIA - Modelos de Datos Extendidos

Este módulo contiene los modelos adicionales para:
- Gestión de casos
- Transferencia a abogados
- Precios y servicios
- Reseñas y reputación
- Consentimiento del usuario
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Text,
    ForeignKey, Float, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


# ============================================================
# ENUMS
# ============================================================

class CaseStatus(enum.Enum):
    """Estados posibles de un caso"""
    DRAFT = "draft"                    # Borrador, aún en chat
    READY_TO_TRANSFER = "ready"        # Listo para transferir
    PENDING_CONSENT = "pending_consent" # Esperando consentimiento
    TRANSFERRED = "transferred"         # Transferido a abogado
    IN_PROGRESS = "in_progress"        # Abogado trabajando
    COMPLETED = "completed"            # Caso cerrado exitosamente
    CANCELLED = "cancelled"            # Cancelado por usuario
    ARCHIVED = "archived"              # Archivado


class CasePriority(enum.Enum):
    """Prioridad del caso"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ConsentType(enum.Enum):
    """Tipos de consentimiento"""
    SHARE_CHAT = "share_chat"           # Compartir historial de chat
    SHARE_DOCUMENTS = "share_documents" # Compartir documentos
    SHARE_CONTACT = "share_contact"     # Compartir datos de contacto
    TRANSFER_CASE = "transfer_case"     # Transferir caso a abogado


class ServiceType(enum.Enum):
    """Tipos de servicio de abogados"""
    INITIAL_CONSULTATION = "initial_consultation"  # Consulta inicial
    HOURLY = "hourly"                               # Por hora
    FIXED_FEE = "fixed_fee"                         # Tarifa fija
    CONTINGENCY = "contingency"                     # Por resultado
    SUBSCRIPTION = "subscription"                    # Suscripción


# ============================================================
# MODELOS DE CASOS
# ============================================================

class Case(Base):
    """
    Caso legal genérico.

    Representa un caso desde que el usuario inicia la conversación
    hasta que se cierra o archiva.
    """
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)

    # Identificador único del caso (LEIA-2025-00001)
    case_number = Column(String(50), unique=True, index=True)

    # Información básica
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=True)  # Resumen generado por IA
    description = Column(Text, nullable=True)  # Descripción del usuario

    # Clasificación
    legal_area = Column(String(100), nullable=True)  # Área legal principal
    sub_area = Column(String(100), nullable=True)    # Sub-área
    priority = Column(SQLEnum(CasePriority), default=CasePriority.MEDIUM)

    # Estado
    status = Column(SQLEnum(CaseStatus), default=CaseStatus.DRAFT)

    # Ubicación del caso
    region = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    comuna = Column(String(100), nullable=True)

    # Fechas relevantes del caso (no del sistema)
    incident_date = Column(DateTime(timezone=True), nullable=True)
    deadline_date = Column(DateTime(timezone=True), nullable=True)

    # Análisis de riesgo (1-10)
    risk_level = Column(Integer, nullable=True)
    risk_factors = Column(JSON, nullable=True)  # Lista de factores de riesgo

    # Datos estructurados extraídos del chat
    extracted_facts = Column(JSON, nullable=True)
    extracted_dates = Column(JSON, nullable=True)
    pending_questions = Column(JSON, nullable=True)

    # Abogado asignado (si hay)
    assigned_lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    transferred_at = Column(DateTime(timezone=True), nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", backref="cases")
    conversation = relationship("Conversation", backref="case")
    assigned_lawyer = relationship("Lawyer", backref="assigned_cases")
    consents = relationship("Consent", back_populates="case", cascade="all, delete-orphan")
    transfers = relationship("CaseTransfer", back_populates="case", cascade="all, delete-orphan")
    documents = relationship("CaseDocument", back_populates="case", cascade="all, delete-orphan")
    timeline = relationship("CaseEvent", back_populates="case", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Case {self.case_number}: {self.title}>"


class CaseTransfer(Base):
    """
    Registro de transferencia de caso a abogado.

    Cada transferencia queda registrada para auditoría.
    """
    __tablename__ = "case_transfers"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False)

    # Estado de la transferencia
    status = Column(String(50), default="pending")  # pending, accepted, rejected, completed

    # Mensaje del usuario al abogado
    user_message = Column(Text, nullable=True)

    # Respuesta del abogado
    lawyer_response = Column(Text, nullable=True)
    response_at = Column(DateTime(timezone=True), nullable=True)

    # Precio acordado (si aplica)
    agreed_price = Column(Integer, nullable=True)
    service_type = Column(SQLEnum(ServiceType), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    case = relationship("Case", back_populates="transfers")
    lawyer = relationship("Lawyer", backref="received_transfers")

    def __repr__(self):
        return f"<CaseTransfer {self.case_id} -> Lawyer {self.lawyer_id}>"


class CaseDocument(Base):
    """Documentos adjuntos a un caso"""
    __tablename__ = "case_documents"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Información del archivo
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=True)  # pdf, docx, jpg, etc.
    file_size = Column(Integer, nullable=True)  # en bytes
    storage_path = Column(String(500), nullable=False)  # ruta en storage

    # Descripción
    description = Column(Text, nullable=True)

    # Control de acceso
    shared_with_lawyer = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    case = relationship("Case", back_populates="documents")
    uploaded_by = relationship("User", backref="uploaded_documents")

    def __repr__(self):
        return f"<CaseDocument {self.filename}>"


class CaseEvent(Base):
    """
    Timeline de eventos del caso.

    Registra cada acción importante para auditoría.
    """
    __tablename__ = "case_events"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Quien hizo la acción

    # Tipo de evento
    event_type = Column(String(100), nullable=False)
    # Ejemplos: created, status_changed, transferred, document_added,
    #           consent_given, lawyer_responded, completed, etc.

    # Detalles del evento
    description = Column(Text, nullable=True)
    event_data = Column(JSON, nullable=True)  # Datos adicionales del evento

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    case = relationship("Case", back_populates="timeline")
    actor = relationship("User", backref="case_events")

    def __repr__(self):
        return f"<CaseEvent {self.event_type} on Case {self.case_id}>"


# ============================================================
# CONSENTIMIENTO
# ============================================================

class Consent(Base):
    """
    Registro de consentimientos del usuario.

    Cada tipo de consentimiento se registra por separado.
    """
    __tablename__ = "consents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)

    # Tipo de consentimiento
    consent_type = Column(SQLEnum(ConsentType), nullable=False)

    # Estado
    granted = Column(Boolean, default=False)

    # Texto exacto que el usuario aceptó
    consent_text = Column(Text, nullable=False)

    # IP y timestamp para auditoría
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Timestamps
    granted_at = Column(DateTime(timezone=True), nullable=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", backref="consents")
    case = relationship("Case", back_populates="consents")

    def __repr__(self):
        return f"<Consent {self.consent_type.value} for User {self.user_id}>"


# ============================================================
# PRECIOS Y SERVICIOS DE ABOGADOS
# ============================================================

class LawyerService(Base):
    """
    Servicios ofrecidos por un abogado con sus precios.
    """
    __tablename__ = "lawyer_services"

    id = Column(Integer, primary_key=True, index=True)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False)

    # Tipo de servicio
    service_type = Column(SQLEnum(ServiceType), nullable=False)

    # Nombre del servicio
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Precio
    price = Column(Integer, nullable=False)  # en CLP
    price_unit = Column(String(50), default="CLP")  # CLP, UF, etc.

    # Duración (para consultas)
    duration_minutes = Column(Integer, nullable=True)  # ej: 30, 60

    # Áreas legales aplicables
    legal_areas = Column(JSON, nullable=True)  # ["Laboral", "Familia"]

    # Estado
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    lawyer = relationship("Lawyer", backref="services")

    def __repr__(self):
        return f"<LawyerService {self.name}: ${self.price}>"


# ============================================================
# RESEÑAS Y REPUTACIÓN
# ============================================================

class Review(Base):
    """
    Reseñas de usuarios sobre abogados.
    """
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)  # Caso relacionado

    # Calificación
    rating = Column(Float, nullable=False)  # 1-5

    # Calificaciones específicas (opcional)
    rating_communication = Column(Float, nullable=True)  # 1-5
    rating_knowledge = Column(Float, nullable=True)       # 1-5
    rating_professionalism = Column(Float, nullable=True) # 1-5
    rating_value = Column(Float, nullable=True)           # 1-5 (relación calidad/precio)

    # Texto de la reseña
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)

    # ¿Recomendaría a este abogado?
    would_recommend = Column(Boolean, nullable=True)

    # Moderación
    is_approved = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    moderation_notes = Column(Text, nullable=True)
    moderated_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    moderated_at = Column(DateTime(timezone=True), nullable=True)

    # Respuesta del abogado
    lawyer_response = Column(Text, nullable=True)
    lawyer_response_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    lawyer = relationship("Lawyer", backref="reviews_received")
    user = relationship("User", foreign_keys=[user_id], backref="reviews_given")
    moderator = relationship("User", foreign_keys=[moderated_by_id])

    def __repr__(self):
        return f"<Review {self.rating}/5 for Lawyer {self.lawyer_id}>"


class LawyerMetrics(Base):
    """
    Métricas internas de rendimiento del abogado.

    Se actualizan automáticamente.
    """
    __tablename__ = "lawyer_metrics"

    id = Column(Integer, primary_key=True, index=True)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False, unique=True)

    # Métricas de respuesta
    avg_response_time_hours = Column(Float, nullable=True)  # Tiempo promedio de respuesta
    response_rate = Column(Float, nullable=True)  # % de casos respondidos

    # Métricas de casos
    total_cases = Column(Integer, default=0)
    completed_cases = Column(Integer, default=0)
    success_rate = Column(Float, nullable=True)  # % casos exitosos

    # Métricas de satisfacción
    avg_rating = Column(Float, nullable=True)
    total_reviews = Column(Integer, default=0)
    recommendation_rate = Column(Float, nullable=True)  # % que recomendarían

    # Métricas de reclamos
    total_complaints = Column(Integer, default=0)
    resolved_complaints = Column(Integer, default=0)

    # Última actualización
    last_calculated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    lawyer = relationship("Lawyer", backref="metrics", uselist=False)

    def __repr__(self):
        return f"<LawyerMetrics for Lawyer {self.lawyer_id}>"


# ============================================================
# FUNCIÓN PARA GENERAR NÚMERO DE CASO
# ============================================================

# ============================================================
# ENUMS PARA COMUNICACIÓN
# ============================================================

class MessageType(enum.Enum):
    """Tipos de mensaje en el chat del caso"""
    TEXT = "text"
    FILE = "file"
    CALL_REQUEST = "call_request"
    SYSTEM = "system"


class CallType(enum.Enum):
    """Tipos de llamada"""
    VOICE = "voice"
    VIDEO = "video"


class CallStatus(enum.Enum):
    """Estados de una llamada"""
    PENDING = "pending"
    RINGING = "ringing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MISSED = "missed"
    REJECTED = "rejected"
    FAILED = "failed"


class NotificationType(enum.Enum):
    """Tipos de notificación"""
    NEW_CASE = "new_case"
    CASE_ACCEPTED = "case_accepted"
    CASE_REJECTED = "case_rejected"
    NEW_MESSAGE = "new_message"
    CALL_REQUEST = "call_request"
    CALL_MISSED = "call_missed"
    DOCUMENT_SHARED = "document_shared"
    CASE_COMPLETED = "case_completed"


# ============================================================
# MODELOS DE COMUNICACIÓN
# ============================================================

class CaseMessage(Base):
    """
    Mensajes entre usuario y abogado dentro de un caso.
    """
    __tablename__ = "case_messages"

    id = Column(Integer, primary_key=True, index=True)
    transfer_id = Column(Integer, ForeignKey("case_transfers.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender_type = Column(String(20), nullable=False)  # 'user' or 'lawyer'

    # Contenido del mensaje
    content = Column(Text, nullable=False)
    message_type = Column(SQLEnum(MessageType), default=MessageType.TEXT)

    # Archivo adjunto (si aplica)
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)

    # Estado de lectura
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    transfer = relationship("CaseTransfer", backref="messages")
    sender = relationship("User", backref="sent_case_messages")

    def __repr__(self):
        return f"<CaseMessage {self.id} from {self.sender_type}>"


class LawyerCommunicationSettings(Base):
    """
    Configuración de comunicación del abogado.
    Define qué métodos de comunicación tiene habilitados.
    """
    __tablename__ = "lawyer_communication_settings"

    id = Column(Integer, primary_key=True, index=True)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False, unique=True)

    # Métodos de comunicación habilitados
    chat_enabled = Column(Boolean, default=True)
    voice_enabled = Column(Boolean, default=False)
    video_enabled = Column(Boolean, default=False)

    # Horarios de disponibilidad (JSON con formato {"monday": {"start": "09:00", "end": "18:00"}, ...})
    available_hours = Column(JSON, nullable=True)

    # Objetivo de tiempo de respuesta en horas
    response_time_target = Column(Integer, default=24)

    # Estado de disponibilidad
    is_available = Column(Boolean, default=True)
    unavailable_until = Column(DateTime(timezone=True), nullable=True)
    unavailable_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    lawyer = relationship("Lawyer", backref="communication_settings", uselist=False)

    def __repr__(self):
        return f"<LawyerCommunicationSettings for Lawyer {self.lawyer_id}>"


class CallSession(Base):
    """
    Sesión de llamada entre usuario y abogado.
    """
    __tablename__ = "call_sessions"

    id = Column(Integer, primary_key=True, index=True)
    transfer_id = Column(Integer, ForeignKey("case_transfers.id"), nullable=False)
    initiated_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Tipo y estado de la llamada
    call_type = Column(SQLEnum(CallType), nullable=False)
    status = Column(SQLEnum(CallStatus), default=CallStatus.PENDING)

    # Información de la sala (para WebRTC/Daily.co)
    room_id = Column(String(100), nullable=True)
    room_url = Column(String(500), nullable=True)

    # Tiempos
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    transfer = relationship("CaseTransfer", backref="calls")
    initiator = relationship("User", backref="initiated_calls")

    def __repr__(self):
        return f"<CallSession {self.id} ({self.call_type.value})>"


class Notification(Base):
    """
    Notificaciones del sistema para usuarios.
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Tipo y contenido
    type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Referencia al caso relacionado
    related_case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)
    related_transfer_id = Column(Integer, ForeignKey("case_transfers.id"), nullable=True)

    # URL de acción
    action_url = Column(String(500), nullable=True)

    # Estado
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True), nullable=True)

    # Datos adicionales (JSON)
    extra_data = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", backref="notifications")
    related_case = relationship("Case", backref="notifications")
    related_transfer = relationship("CaseTransfer", backref="notifications")

    def __repr__(self):
        return f"<Notification {self.id}: {self.type.value}>"


# ============================================================
# FUNCIÓN PARA GENERAR NÚMERO DE CASO
# ============================================================

def generate_case_number(db_session) -> str:
    """
    Genera un número de caso único.
    Formato: LEIA-YYYY-NNNNN
    """
    from datetime import datetime

    year = datetime.now().year
    prefix = f"LEIA-{year}-"

    # Buscar el último número del año
    last_case = db_session.query(Case).filter(
        Case.case_number.like(f"{prefix}%")
    ).order_by(Case.id.desc()).first()

    if last_case:
        last_number = int(last_case.case_number.split("-")[-1])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"{prefix}{new_number:05d}"
