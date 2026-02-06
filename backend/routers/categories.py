"""
Router para categorías legales.
"""
from fastapi import APIRouter
from typing import List, Dict, Optional

from services.legal_categories import (
    get_all_categories,
    get_category,
    get_category_by_keyword,
    LEGAL_CATEGORIES
)

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/")
async def list_categories() -> List[Dict]:
    """
    Lista todas las categorías legales disponibles.
    """
    return get_all_categories()


@router.get("/{category_id}")
async def get_category_detail(category_id: str) -> Dict:
    """
    Obtiene el detalle de una categoría específica.
    """
    category = get_category(category_id)
    if not category:
        return {"error": "Categoría no encontrada"}

    return {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "icon": category.icon,
        "subcategories": category.subcategories,
        "referral_triggers": category.referral_triggers
    }


@router.get("/{category_id}/subcategories")
async def get_subcategories(category_id: str) -> List[str]:
    """
    Obtiene las subcategorías de una categoría.
    """
    category = get_category(category_id)
    if not category:
        return []
    return category.subcategories


@router.post("/detect")
async def detect_category(text: str) -> Dict:
    """
    Detecta la categoría más probable basándose en el texto.
    """
    category_id = get_category_by_keyword(text)
    if not category_id:
        return {"category": None, "confidence": 0}

    category = get_category(category_id)
    return {
        "category": {
            "id": category.id,
            "name": category.name
        },
        "confidence": 0.8  # Simplificado, podría mejorarse
    }
