"""
API endpoints for direct chat between users and lawyers.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import get_db
from auth import get_current_user
from models import User, Lawyer, DirectConversation, DirectMessage

router = APIRouter(prefix="/api/chat/direct", tags=["Direct Chat"])


# ==================== SCHEMAS ====================

class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    sender_type: str
    sender_name: str
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: int
    other_party_name: str
    other_party_id: int
    other_party_type: str  # user or lawyer
    last_message: Optional[str]
    last_message_at: Optional[datetime]
    unread_count: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationDetailResponse(BaseModel):
    id: int
    other_party_name: str
    other_party_id: int
    case_summary: Optional[str]
    status: str
    messages: List[MessageResponse]


class StartConversationRequest(BaseModel):
    lawyer_id: int
    initial_message: str
    case_summary: Optional[str] = None


# ==================== ENDPOINTS ====================

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for the current user."""

    # Check if user is a lawyer
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if lawyer:
        # Get conversations where user is the lawyer
        conversations = db.query(DirectConversation).filter(
            DirectConversation.lawyer_id == lawyer.id
        ).order_by(desc(DirectConversation.last_message_at)).all()

        result = []
        for conv in conversations:
            # Get last message
            last_msg = db.query(DirectMessage).filter(
                DirectMessage.conversation_id == conv.id
            ).order_by(desc(DirectMessage.created_at)).first()

            # Get user info
            user = db.query(User).filter(User.id == conv.user_id).first()

            result.append(ConversationResponse(
                id=conv.id,
                other_party_name=user.full_name or user.email,
                other_party_id=user.id,
                other_party_type="user",
                last_message=last_msg.content[:100] if last_msg else None,
                last_message_at=conv.last_message_at,
                unread_count=conv.unread_lawyer,
                status=conv.status,
                created_at=conv.created_at
            ))
        return result
    else:
        # Get conversations where user is the client
        conversations = db.query(DirectConversation).filter(
            DirectConversation.user_id == current_user.id
        ).order_by(desc(DirectConversation.last_message_at)).all()

        result = []
        for conv in conversations:
            # Get last message
            last_msg = db.query(DirectMessage).filter(
                DirectMessage.conversation_id == conv.id
            ).order_by(desc(DirectMessage.created_at)).first()

            # Get lawyer info
            lawyer_info = db.query(Lawyer).filter(Lawyer.id == conv.lawyer_id).first()

            result.append(ConversationResponse(
                id=conv.id,
                other_party_name=lawyer_info.name if lawyer_info else "Abogado",
                other_party_id=conv.lawyer_id,
                other_party_type="lawyer",
                last_message=last_msg.content[:100] if last_msg else None,
                last_message_at=conv.last_message_at,
                unread_count=conv.unread_user,
                status=conv.status,
                created_at=conv.created_at
            ))
        return result


@router.post("/conversations", response_model=ConversationDetailResponse)
async def start_conversation(
    request: StartConversationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new conversation with a lawyer."""

    # Check if lawyer exists
    lawyer = db.query(Lawyer).filter(Lawyer.id == request.lawyer_id).first()
    if not lawyer:
        raise HTTPException(status_code=404, detail="Abogado no encontrado")

    # Check if conversation already exists
    existing = db.query(DirectConversation).filter(
        and_(
            DirectConversation.user_id == current_user.id,
            DirectConversation.lawyer_id == request.lawyer_id,
            DirectConversation.status == "active"
        )
    ).first()

    if existing:
        # Return existing conversation
        messages = db.query(DirectMessage).filter(
            DirectMessage.conversation_id == existing.id
        ).order_by(DirectMessage.created_at).all()

        return ConversationDetailResponse(
            id=existing.id,
            other_party_name=lawyer.name,
            other_party_id=lawyer.id,
            case_summary=existing.case_summary,
            status=existing.status,
            messages=[
                MessageResponse(
                    id=m.id,
                    sender_id=m.sender_id,
                    sender_type=m.sender_type,
                    sender_name=current_user.full_name if m.sender_type == "user" else lawyer.name,
                    content=m.content,
                    is_read=m.is_read,
                    created_at=m.created_at
                ) for m in messages
            ]
        )

    # Create new conversation
    conversation = DirectConversation(
        user_id=current_user.id,
        lawyer_id=request.lawyer_id,
        case_summary=request.case_summary,
        last_message_at=datetime.utcnow(),
        unread_lawyer=1
    )
    db.add(conversation)
    db.flush()

    # Add initial message
    message = DirectMessage(
        conversation_id=conversation.id,
        sender_id=current_user.id,
        sender_type="user",
        content=request.initial_message
    )
    db.add(message)
    db.commit()
    db.refresh(conversation)
    db.refresh(message)

    return ConversationDetailResponse(
        id=conversation.id,
        other_party_name=lawyer.name,
        other_party_id=lawyer.id,
        case_summary=conversation.case_summary,
        status=conversation.status,
        messages=[
            MessageResponse(
                id=message.id,
                sender_id=message.sender_id,
                sender_type=message.sender_type,
                sender_name=current_user.full_name or "Usuario",
                content=message.content,
                is_read=message.is_read,
                created_at=message.created_at
            )
        ]
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific conversation with all messages."""

    conversation = db.query(DirectConversation).filter(
        DirectConversation.id == conversation_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversacion no encontrada")

    # Check access
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()
    is_lawyer = lawyer and lawyer.id == conversation.lawyer_id
    is_user = conversation.user_id == current_user.id

    if not is_lawyer and not is_user:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta conversacion")

    # Mark messages as read
    if is_user:
        conversation.unread_user = 0
        db.query(DirectMessage).filter(
            and_(
                DirectMessage.conversation_id == conversation_id,
                DirectMessage.sender_type == "lawyer"
            )
        ).update({"is_read": True})
    else:
        conversation.unread_lawyer = 0
        db.query(DirectMessage).filter(
            and_(
                DirectMessage.conversation_id == conversation_id,
                DirectMessage.sender_type == "user"
            )
        ).update({"is_read": True})

    db.commit()

    # Get messages
    messages = db.query(DirectMessage).filter(
        DirectMessage.conversation_id == conversation_id
    ).order_by(DirectMessage.created_at).all()

    # Get other party info
    if is_user:
        lawyer_info = db.query(Lawyer).filter(Lawyer.id == conversation.lawyer_id).first()
        other_name = lawyer_info.name if lawyer_info else "Abogado"
        other_id = conversation.lawyer_id
    else:
        user_info = db.query(User).filter(User.id == conversation.user_id).first()
        other_name = user_info.full_name or user_info.email if user_info else "Usuario"
        other_id = conversation.user_id

    return ConversationDetailResponse(
        id=conversation.id,
        other_party_name=other_name,
        other_party_id=other_id,
        case_summary=conversation.case_summary,
        status=conversation.status,
        messages=[
            MessageResponse(
                id=m.id,
                sender_id=m.sender_id,
                sender_type=m.sender_type,
                sender_name=get_sender_name(db, m, conversation),
                content=m.content,
                is_read=m.is_read,
                created_at=m.created_at
            ) for m in messages
        ]
    )


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    request: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in a conversation."""

    conversation = db.query(DirectConversation).filter(
        DirectConversation.id == conversation_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversacion no encontrada")

    # Check access and determine sender type
    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()
    is_lawyer = lawyer and lawyer.id == conversation.lawyer_id
    is_user = conversation.user_id == current_user.id

    if not is_lawyer and not is_user:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta conversacion")

    sender_type = "lawyer" if is_lawyer else "user"

    # Create message
    message = DirectMessage(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        sender_type=sender_type,
        content=request.content
    )
    db.add(message)

    # Update conversation
    conversation.last_message_at = datetime.utcnow()
    if sender_type == "user":
        conversation.unread_lawyer += 1
    else:
        conversation.unread_user += 1

    db.commit()
    db.refresh(message)

    return MessageResponse(
        id=message.id,
        sender_id=message.sender_id,
        sender_type=message.sender_type,
        sender_name=current_user.full_name or "Usuario",
        content=message.content,
        is_read=message.is_read,
        created_at=message.created_at
    )


@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get total unread message count."""

    lawyer = db.query(Lawyer).filter(Lawyer.user_id == current_user.id).first()

    if lawyer:
        total = db.query(DirectConversation).filter(
            DirectConversation.lawyer_id == lawyer.id
        ).with_entities(
            db.query(DirectConversation.unread_lawyer).scalar_subquery()
        ).scalar() or 0
    else:
        total = db.query(DirectConversation).filter(
            DirectConversation.user_id == current_user.id
        ).with_entities(
            db.query(DirectConversation.unread_user).scalar_subquery()
        ).scalar() or 0

    return {"unread_count": total}


# Helper function
def get_sender_name(db: Session, message: DirectMessage, conversation: DirectConversation) -> str:
    if message.sender_type == "user":
        user = db.query(User).filter(User.id == conversation.user_id).first()
        return user.full_name or user.email if user else "Usuario"
    else:
        lawyer = db.query(Lawyer).filter(Lawyer.id == conversation.lawyer_id).first()
        return lawyer.name if lawyer else "Abogado"
