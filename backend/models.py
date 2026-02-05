"""
Database models for JusticiaAI.
"""
import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class ProfessionalType(enum.Enum):
    """Type of legal professional."""
    ABOGADO = "abogado"           # Full lawyer - can do everything
    PROCURADOR = "procurador"     # Court agent - limited functions
    ESTUDIO = "estudio"           # Law firm - manages multiple lawyers


class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(50), default="user")  # user, lawyer, admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    conversations = relationship("Conversation", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"


class Conversation(Base):
    """Stores chat conversation history for users."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), index=True)  # For anonymous users
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ChatMessage", back_populates="conversation")


class ChatMessage(Base):
    """Individual messages within a conversation."""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class Feedback(Base):
    """Stores user feedback on AI responses."""
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(100), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_question = Column(Text, nullable=True)
    ai_response = Column(Text, nullable=True)
    feedback = Column(String(20), nullable=False)  # helpful, not_helpful
    correction = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Lawyer(Base):
    """Stores lawyer profiles for the marketplace."""
    __tablename__ = "lawyers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String(255), nullable=False)
    professional_type = Column(Enum(ProfessionalType), default=ProfessionalType.ABOGADO, nullable=False)
    specialty = Column(String(100), nullable=False)
    experience = Column(String(50), nullable=True)
    rating = Column(Float, default=0)
    reviews = Column(Integer, default=0)
    location = Column(String(100), nullable=True)
    price_min = Column(Integer, nullable=True)
    price_max = Column(Integer, nullable=True)
    image = Column(String(500), nullable=True)
    cases = Column(Integer, default=0)
    success_rate = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    phone = Column(String(50), nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="lawyer_profile")
    consultations = relationship("Consultation", back_populates="lawyer")

    def __repr__(self):
        return f"<Lawyer {self.name} ({self.professional_type.value})>"


class Consultation(Base):
    """Stores consultation requests from users to lawyers."""
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="pending")  # pending, contacted, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    lawyer = relationship("Lawyer", back_populates="consultations")

    def __repr__(self):
        return f"<Consultation {self.id} - {self.name}>"


class PJUDConnection(Base):
    """Stores user connection to Poder Judicial via ClaveÚnica."""
    __tablename__ = "pjud_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    rut = Column(String(20), nullable=False)
    # Credenciales encriptadas - en producción usar vault o similar
    encrypted_credentials = Column(Text, nullable=True)
    is_connected = Column(Boolean, default=False)
    last_sync = Column(DateTime(timezone=True), nullable=True)
    sync_status = Column(String(50), default="pending")  # pending, syncing, success, error
    sync_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="pjud_connection")
    causas = relationship("CausaJudicial", back_populates="connection", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PJUDConnection {self.rut}>"


class CausaJudicial(Base):
    """Stores judicial cases from Poder Judicial."""
    __tablename__ = "causas_judiciales"

    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("pjud_connections.id"), nullable=False)
    rit = Column(String(50), nullable=False, index=True)
    tribunal = Column(String(255), nullable=True)
    caratulado = Column(String(500), nullable=True)
    materia = Column(String(255), nullable=True)
    estado = Column(String(100), nullable=True)
    fecha_ingreso = Column(String(50), nullable=True)
    ultima_actuacion = Column(Text, nullable=True)
    fecha_actuacion = Column(String(50), nullable=True)
    proxima_audiencia = Column(String(50), nullable=True)
    datos_raw = Column(Text, nullable=True)  # JSON con datos adicionales
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    connection = relationship("PJUDConnection", back_populates="causas")

    def __repr__(self):
        return f"<CausaJudicial {self.rit}>"


class DirectConversation(Base):
    """Chat conversation between user and lawyer."""
    __tablename__ = "direct_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lawyer_id = Column(Integer, ForeignKey("lawyers.id"), nullable=False)
    case_summary = Column(Text, nullable=True)  # Summary from LEIA chat
    status = Column(String(50), default="active")  # active, archived, closed
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    unread_user = Column(Integer, default=0)  # Unread count for user
    unread_lawyer = Column(Integer, default=0)  # Unread count for lawyer
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="direct_conversations")
    lawyer = relationship("Lawyer", backref="direct_conversations")
    messages = relationship("DirectMessage", back_populates="conversation", order_by="DirectMessage.created_at")

    def __repr__(self):
        return f"<DirectConversation {self.id}>"


class DirectMessage(Base):
    """Individual message in a direct conversation."""
    __tablename__ = "direct_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("direct_conversations.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender_type = Column(String(20), nullable=False)  # user, lawyer
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation = relationship("DirectConversation", back_populates="messages")
    sender = relationship("User", backref="sent_messages")

    def __repr__(self):
        return f"<DirectMessage {self.id}>"
