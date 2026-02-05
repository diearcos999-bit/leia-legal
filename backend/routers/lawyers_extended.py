"""
LEIA - Router de Abogados Extendido

Endpoints para:
- Listado con filtros avanzados
- Servicios y precios
- Reseñas y métricas
- Matching inteligente
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from database import get_db
from auth import get_current_user, get_current_user_optional
from models import User, Lawyer
from models_extended import (
    LawyerService, Review, LawyerMetrics,
    ServiceType, Case
)

router = APIRouter(prefix="/api/lawyers", tags=["lawyers-extended"])


# ============================================================
# SCHEMAS
# ============================================================

class ServiceResponse(BaseModel):
    """Respuesta de servicio"""
    id: int
    service_type: ServiceType
    name: str
    description: Optional[str]
    price: int
    price_unit: str
    duration_minutes: Optional[int]
    legal_areas: Optional[List[str]]

    class Config:
        from_attributes = True


class LawyerDetailResponse(BaseModel):
    """Respuesta detallada de abogado"""
    id: int
    name: str
    specialty: str
    experience: Optional[str]
    rating: float
    reviews_count: int
    location: Optional[str]
    description: Optional[str]
    is_verified: bool
    cases_completed: int
    success_rate: Optional[float]
    services: List[ServiceResponse]
    avg_response_time: Optional[str]
    recommendation_rate: Optional[float]


class ReviewCreate(BaseModel):
    """Crear una reseña"""
    case_id: Optional[int] = None
    rating: float = Field(..., ge=1, le=5)
    rating_communication: Optional[float] = Field(None, ge=1, le=5)
    rating_knowledge: Optional[float] = Field(None, ge=1, le=5)
    rating_professionalism: Optional[float] = Field(None, ge=1, le=5)
    rating_value: Optional[float] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = Field(None, max_length=2000)
    would_recommend: Optional[bool] = None


class ReviewResponse(BaseModel):
    """Respuesta de reseña"""
    id: int
    rating: float
    title: Optional[str]
    content: Optional[str]
    would_recommend: Optional[bool]
    created_at: datetime
    lawyer_response: Optional[str]

    class Config:
        from_attributes = True


class LawyerMatchRequest(BaseModel):
    """Solicitud de matching de abogado"""
    legal_area: str
    region: Optional[str] = None
    city: Optional[str] = None
    priority: Optional[str] = None  # low, medium, high, urgent
    max_price: Optional[int] = None
    min_rating: Optional[float] = Field(None, ge=1, le=5)


class LawyerMatchResponse(BaseModel):
    """Resultado del matching"""
    lawyers: List[Dict[str, Any]]
    total_matches: int
    filters_applied: Dict[str, Any]


# ============================================================
# ENDPOINTS DE BÚSQUEDA AVANZADA
# ============================================================

@router.get("/search", response_model=LawyerMatchResponse)
async def search_lawyers(
    legal_area: Optional[str] = None,
    region: Optional[str] = None,
    city: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=1, le=5),
    max_price: Optional[int] = None,
    service_type: Optional[ServiceType] = None,
    verified_only: bool = True,
    sort_by: str = Query("rating", regex="^(rating|price|response_time|cases)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Búsqueda avanzada de abogados con múltiples filtros.
    """
    query = db.query(Lawyer)

    filters_applied = {}

    # Filtro por verificación
    if verified_only:
        query = query.filter(Lawyer.is_verified == True)
        filters_applied["verified_only"] = True

    # Filtro por especialidad
    if legal_area:
        query = query.filter(Lawyer.specialty.ilike(f"%{legal_area}%"))
        filters_applied["legal_area"] = legal_area

    # Filtro por ubicación
    if region:
        query = query.filter(Lawyer.location.ilike(f"%{region}%"))
        filters_applied["region"] = region

    # Filtro por rating mínimo
    if min_rating:
        query = query.filter(Lawyer.rating >= min_rating)
        filters_applied["min_rating"] = min_rating

    # Filtro por precio máximo (consulta inicial)
    if max_price:
        query = query.filter(Lawyer.price_min <= max_price)
        filters_applied["max_price"] = max_price

    # Contar total antes de paginar
    total = query.count()

    # Ordenamiento
    if sort_by == "rating":
        query = query.order_by(Lawyer.rating.desc())
    elif sort_by == "price":
        query = query.order_by(Lawyer.price_min.asc())
    elif sort_by == "cases":
        query = query.order_by(Lawyer.cases.desc())
    else:
        query = query.order_by(Lawyer.rating.desc())

    # Paginación
    offset = (page - 1) * page_size
    lawyers = query.offset(offset).limit(page_size).all()

    # Formatear respuesta
    results = []
    for lawyer in lawyers:
        # Obtener servicios
        services = db.query(LawyerService).filter(
            and_(
                LawyerService.lawyer_id == lawyer.id,
                LawyerService.is_active == True
            )
        ).all()

        # Obtener métricas
        metrics = db.query(LawyerMetrics).filter(
            LawyerMetrics.lawyer_id == lawyer.id
        ).first()

        # Formatear precio
        price_display = None
        if lawyer.price_min and lawyer.price_max:
            price_display = f"${lawyer.price_min:,} - ${lawyer.price_max:,}".replace(",", ".")
        elif lawyer.price_min:
            price_display = f"Desde ${lawyer.price_min:,}".replace(",", ".")

        results.append({
            "id": lawyer.id,
            "name": lawyer.name,
            "specialty": lawyer.specialty,
            "experience": lawyer.experience,
            "rating": lawyer.rating or 0,
            "reviews_count": lawyer.reviews or 0,
            "location": lawyer.location,
            "price_display": price_display,
            "price_min": lawyer.price_min,
            "price_max": lawyer.price_max,
            "is_verified": lawyer.is_verified,
            "cases_completed": lawyer.cases or 0,
            "success_rate": lawyer.success_rate,
            "image": lawyer.image,
            "services_count": len(services),
            "avg_response_time": f"{metrics.avg_response_time_hours:.0f}h" if metrics and metrics.avg_response_time_hours else None,
            "recommendation_rate": metrics.recommendation_rate if metrics else None
        })

    return LawyerMatchResponse(
        lawyers=results,
        total_matches=total,
        filters_applied=filters_applied
    )


@router.post("/match", response_model=LawyerMatchResponse)
async def match_lawyers(
    match_request: LawyerMatchRequest,
    db: Session = Depends(get_db)
):
    """
    Matching inteligente de abogados basado en el caso.

    Prioriza:
    1. Coincidencia de área legal
    2. Ubicación cercana
    3. Rating alto
    4. Tiempo de respuesta rápido
    5. Precio dentro del rango
    """
    query = db.query(Lawyer).filter(Lawyer.is_verified == True)

    # Filtro por área legal (obligatorio)
    query = query.filter(
        or_(
            Lawyer.specialty.ilike(f"%{match_request.legal_area}%"),
            Lawyer.description.ilike(f"%{match_request.legal_area}%")
        )
    )

    # Filtro por región
    if match_request.region:
        query = query.filter(Lawyer.location.ilike(f"%{match_request.region}%"))

    # Filtro por rating mínimo
    if match_request.min_rating:
        query = query.filter(Lawyer.rating >= match_request.min_rating)

    # Filtro por precio
    if match_request.max_price:
        query = query.filter(Lawyer.price_min <= match_request.max_price)

    # Ordenar por rating y casos
    query = query.order_by(Lawyer.rating.desc(), Lawyer.cases.desc())

    lawyers = query.limit(10).all()

    results = []
    for lawyer in lawyers:
        # Calcular score de match (0-100)
        match_score = 50  # Base

        # +20 por rating alto
        if lawyer.rating and lawyer.rating >= 4.5:
            match_score += 20
        elif lawyer.rating and lawyer.rating >= 4.0:
            match_score += 10

        # +15 por experiencia
        if lawyer.cases and lawyer.cases >= 50:
            match_score += 15
        elif lawyer.cases and lawyer.cases >= 20:
            match_score += 10

        # +15 por tasa de éxito
        if lawyer.success_rate and lawyer.success_rate >= 0.9:
            match_score += 15
        elif lawyer.success_rate and lawyer.success_rate >= 0.8:
            match_score += 10

        # Formatear precio
        price_display = None
        if lawyer.price_min and lawyer.price_max:
            price_display = f"${lawyer.price_min:,} - ${lawyer.price_max:,}".replace(",", ".")
        elif lawyer.price_min:
            price_display = f"Desde ${lawyer.price_min:,}".replace(",", ".")

        results.append({
            "id": lawyer.id,
            "name": lawyer.name,
            "specialty": lawyer.specialty,
            "experience": lawyer.experience,
            "rating": lawyer.rating or 0,
            "reviews_count": lawyer.reviews or 0,
            "location": lawyer.location,
            "price_display": price_display,
            "is_verified": lawyer.is_verified,
            "cases_completed": lawyer.cases or 0,
            "success_rate": lawyer.success_rate,
            "image": lawyer.image,
            "match_score": min(match_score, 100)
        })

    # Ordenar por match_score
    results.sort(key=lambda x: x["match_score"], reverse=True)

    return LawyerMatchResponse(
        lawyers=results,
        total_matches=len(results),
        filters_applied={
            "legal_area": match_request.legal_area,
            "region": match_request.region,
            "max_price": match_request.max_price
        }
    )


# ============================================================
# ENDPOINTS DE DETALLE
# ============================================================

@router.get("/{lawyer_id}/full")
async def get_lawyer_full_detail(
    lawyer_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene el perfil completo de un abogado incluyendo servicios y métricas.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abogado no encontrado"
        )

    # Obtener servicios
    services = db.query(LawyerService).filter(
        and_(
            LawyerService.lawyer_id == lawyer_id,
            LawyerService.is_active == True
        )
    ).all()

    # Obtener métricas
    metrics = db.query(LawyerMetrics).filter(
        LawyerMetrics.lawyer_id == lawyer_id
    ).first()

    # Obtener últimas reseñas aprobadas
    reviews = db.query(Review).filter(
        and_(
            Review.lawyer_id == lawyer_id,
            Review.is_approved == True,
            Review.is_visible == True
        )
    ).order_by(Review.created_at.desc()).limit(5).all()

    return {
        "id": lawyer.id,
        "name": lawyer.name,
        "specialty": lawyer.specialty,
        "experience": lawyer.experience,
        "rating": lawyer.rating or 0,
        "reviews_count": lawyer.reviews or 0,
        "location": lawyer.location,
        "description": lawyer.description,
        "is_verified": lawyer.is_verified,
        "cases_completed": lawyer.cases or 0,
        "success_rate": lawyer.success_rate,
        "image": lawyer.image,
        "services": [
            {
                "id": s.id,
                "type": s.service_type.value,
                "name": s.name,
                "description": s.description,
                "price": s.price,
                "price_formatted": f"${s.price:,}".replace(",", "."),
                "duration_minutes": s.duration_minutes,
                "legal_areas": s.legal_areas
            }
            for s in services
        ],
        "metrics": {
            "avg_response_time_hours": metrics.avg_response_time_hours if metrics else None,
            "response_rate": metrics.response_rate if metrics else None,
            "total_cases": metrics.total_cases if metrics else 0,
            "completed_cases": metrics.completed_cases if metrics else 0,
            "recommendation_rate": metrics.recommendation_rate if metrics else None
        } if metrics else None,
        "recent_reviews": [
            {
                "rating": r.rating,
                "title": r.title,
                "content": r.content,
                "would_recommend": r.would_recommend,
                "created_at": r.created_at.isoformat(),
                "lawyer_response": r.lawyer_response
            }
            for r in reviews
        ]
    }


# ============================================================
# ENDPOINTS DE SERVICIOS
# ============================================================

@router.get("/{lawyer_id}/services")
async def get_lawyer_services(
    lawyer_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene los servicios y precios de un abogado.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abogado no encontrado"
        )

    services = db.query(LawyerService).filter(
        and_(
            LawyerService.lawyer_id == lawyer_id,
            LawyerService.is_active == True
        )
    ).order_by(LawyerService.price.asc()).all()

    return {
        "lawyer_id": lawyer_id,
        "lawyer_name": lawyer.name,
        "services": [
            {
                "id": s.id,
                "type": s.service_type.value,
                "name": s.name,
                "description": s.description,
                "price": s.price,
                "price_formatted": f"${s.price:,}".replace(",", "."),
                "price_unit": s.price_unit,
                "duration_minutes": s.duration_minutes,
                "duration_display": f"{s.duration_minutes} min" if s.duration_minutes else None,
                "legal_areas": s.legal_areas
            }
            for s in services
        ]
    }


# ============================================================
# ENDPOINTS DE RESEÑAS
# ============================================================

@router.get("/{lawyer_id}/reviews")
async def get_lawyer_reviews(
    lawyer_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Obtiene las reseñas de un abogado.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abogado no encontrado"
        )

    query = db.query(Review).filter(
        and_(
            Review.lawyer_id == lawyer_id,
            Review.is_approved == True,
            Review.is_visible == True
        )
    )

    total = query.count()

    # Estadísticas
    stats = db.query(
        func.avg(Review.rating).label("avg_rating"),
        func.avg(Review.rating_communication).label("avg_communication"),
        func.avg(Review.rating_knowledge).label("avg_knowledge"),
        func.avg(Review.rating_professionalism).label("avg_professionalism"),
        func.avg(Review.rating_value).label("avg_value"),
        func.sum(func.cast(Review.would_recommend, Integer)).label("would_recommend_count")
    ).filter(
        and_(
            Review.lawyer_id == lawyer_id,
            Review.is_approved == True
        )
    ).first()

    # Paginación
    offset = (page - 1) * page_size
    reviews = query.order_by(Review.created_at.desc()).offset(offset).limit(page_size).all()

    return {
        "lawyer_id": lawyer_id,
        "total_reviews": total,
        "statistics": {
            "avg_rating": round(stats.avg_rating, 1) if stats.avg_rating else None,
            "avg_communication": round(stats.avg_communication, 1) if stats.avg_communication else None,
            "avg_knowledge": round(stats.avg_knowledge, 1) if stats.avg_knowledge else None,
            "avg_professionalism": round(stats.avg_professionalism, 1) if stats.avg_professionalism else None,
            "avg_value": round(stats.avg_value, 1) if stats.avg_value else None,
            "recommendation_rate": round((stats.would_recommend_count / total) * 100, 1) if total > 0 and stats.would_recommend_count else None
        },
        "reviews": [
            {
                "id": r.id,
                "rating": r.rating,
                "rating_communication": r.rating_communication,
                "rating_knowledge": r.rating_knowledge,
                "rating_professionalism": r.rating_professionalism,
                "rating_value": r.rating_value,
                "title": r.title,
                "content": r.content,
                "would_recommend": r.would_recommend,
                "created_at": r.created_at.isoformat(),
                "lawyer_response": r.lawyer_response,
                "lawyer_response_at": r.lawyer_response_at.isoformat() if r.lawyer_response_at else None
            }
            for r in reviews
        ],
        "page": page,
        "page_size": page_size
    }


@router.post("/{lawyer_id}/reviews")
async def create_review(
    lawyer_id: int,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea una reseña para un abogado.

    Solo puede reseñar un usuario que haya tenido un caso con el abogado.
    """
    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()

    if not lawyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abogado no encontrado"
        )

    # Verificar que el usuario tuvo un caso con este abogado
    has_case = db.query(Case).filter(
        and_(
            Case.user_id == current_user.id,
            Case.assigned_lawyer_id == lawyer_id,
            Case.status.in_(["in_progress", "completed"])
        )
    ).first()

    if not has_case:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes reseñar abogados con los que hayas trabajado"
        )

    # Verificar que no haya reseñado ya
    existing = db.query(Review).filter(
        and_(
            Review.lawyer_id == lawyer_id,
            Review.user_id == current_user.id
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya has reseñado a este abogado"
        )

    # Crear reseña
    review = Review(
        lawyer_id=lawyer_id,
        user_id=current_user.id,
        case_id=review_data.case_id or has_case.id,
        rating=review_data.rating,
        rating_communication=review_data.rating_communication,
        rating_knowledge=review_data.rating_knowledge,
        rating_professionalism=review_data.rating_professionalism,
        rating_value=review_data.rating_value,
        title=review_data.title,
        content=review_data.content,
        would_recommend=review_data.would_recommend,
        is_approved=False  # Requiere moderación
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "status": "ok",
        "message": "Reseña enviada. Será visible después de moderación.",
        "review_id": review.id
    }


# Importar Integer para la función de agregación
from sqlalchemy import Integer
