"""
API endpoints para integración con Poder Judicial de Chile.
Sincroniza causas judiciales y sus actuaciones.
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import logging

from database import get_db
from auth import get_current_user
from models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/pjud", tags=["Poder Judicial"])


# ==================== SCHEMAS ====================

class PJUDCredentials(BaseModel):
    """Credenciales para ClaveÚnica."""
    rut: str = Field(..., description="RUT sin puntos ni guión (ej: 209769441)")
    password: str = Field(..., description="Contraseña de ClaveÚnica")


class ActuacionResponse(BaseModel):
    """Actuación/trámite de una causa."""
    folio: str
    etapa: str
    tramite: str
    descripcion: str
    fecha: str
    foja: str = ""
    tiene_documento: bool = False


class CausaResponse(BaseModel):
    """Causa judicial con detalles y actuaciones."""
    id: int
    tipo: str
    rit: str
    ruc: str = ""
    tribunal: str
    caratulado: str
    fecha_ingreso: str
    estado: str
    procedimiento: str = ""
    etapa: str = ""
    ultima_actuacion: Optional[str] = None
    fecha_ultima_actuacion: Optional[str] = None
    actuaciones: List[ActuacionResponse] = []
    actuaciones_count: int = 0


class CausasListResponse(BaseModel):
    """Lista de causas del usuario."""
    causas: List[CausaResponse]
    total: int
    last_sync: Optional[str] = None


class SyncResponse(BaseModel):
    """Respuesta de sincronización."""
    success: bool
    message: str
    causas_count: int = 0
    sync_date: Optional[str] = None


class SyncStatusResponse(BaseModel):
    """Estado de sincronización."""
    has_data: bool
    causas_count: int
    last_sync: Optional[str] = None
    is_syncing: bool = False


# ==================== STORAGE ====================
# Almacenamiento temporal en memoria
# En producción, guardar en base de datos

_user_causas: Dict[int, Dict[str, Any]] = {}
_sync_status: Dict[int, bool] = {}  # user_id -> is_syncing


# ==================== ENDPOINTS ====================

@router.post("/sync", response_model=SyncResponse)
async def sync_causas(
    credentials: PJUDCredentials,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Sincroniza las causas del usuario desde el Poder Judicial.

    Proceso 100% automático usando ClaveÚnica.
    """
    user_id = current_user.id

    # Verificar si ya hay sincronización en progreso
    if _sync_status.get(user_id):
        raise HTTPException(
            status_code=400,
            detail="Ya hay una sincronización en progreso"
        )

    try:
        _sync_status[user_id] = True
        logger.info(f"Iniciando sincronización PJUD para usuario {user_id}")

        from services.pjud_scraper import PJUDScraper

        # Limpiar RUT
        rut_clean = credentials.rut.replace(".", "").replace("-", "")

        # Crear scraper y sincronizar
        scraper = PJUDScraper()
        result = await scraper.sync_causas_completas(rut_clean, credentials.password)

        if not result.get('success'):
            raise HTTPException(
                status_code=400,
                detail=result.get('error', 'Error al sincronizar con Poder Judicial')
            )

        # Guardar causas
        _user_causas[user_id] = {
            'causas': result.get('causas', []),
            'last_sync': result.get('sync_date')
        }

        causas_count = len(result.get('causas', []))
        logger.info(f"Sincronización exitosa: {causas_count} causas")

        return SyncResponse(
            success=True,
            message=f"Se sincronizaron {causas_count} causas correctamente",
            causas_count=causas_count,
            sync_date=result.get('sync_date')
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en sincronización PJUD: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        _sync_status[user_id] = False


@router.get("/status", response_model=SyncStatusResponse)
async def get_sync_status(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el estado de sincronización del usuario.
    """
    user_id = current_user.id
    user_data = _user_causas.get(user_id, {})

    return SyncStatusResponse(
        has_data=len(user_data.get('causas', [])) > 0,
        causas_count=len(user_data.get('causas', [])),
        last_sync=user_data.get('last_sync'),
        is_syncing=_sync_status.get(user_id, False)
    )


@router.get("/causas", response_model=CausasListResponse)
async def get_causas(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene las causas sincronizadas del usuario.
    """
    user_id = current_user.id
    user_data = _user_causas.get(user_id, {})
    causas_raw = user_data.get('causas', [])

    # Convertir a response
    causas = []
    for i, c in enumerate(causas_raw):
        actuaciones = [
            ActuacionResponse(**a) for a in c.get('actuaciones', [])
        ]
        causas.append(CausaResponse(
            id=i + 1,
            tipo=c.get('tipo', ''),
            rit=c.get('rit', ''),
            ruc=c.get('ruc', ''),
            tribunal=c.get('tribunal', ''),
            caratulado=c.get('caratulado', ''),
            fecha_ingreso=c.get('fecha_ingreso', ''),
            estado=c.get('estado', ''),
            procedimiento=c.get('procedimiento', ''),
            etapa=c.get('etapa', ''),
            ultima_actuacion=c.get('ultima_actuacion'),
            fecha_ultima_actuacion=c.get('fecha_ultima_actuacion'),
            actuaciones=actuaciones,
            actuaciones_count=len(actuaciones)
        ))

    return CausasListResponse(
        causas=causas,
        total=len(causas),
        last_sync=user_data.get('last_sync')
    )


@router.get("/causas/{causa_id}", response_model=CausaResponse)
async def get_causa_detail(
    causa_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el detalle completo de una causa con todas sus actuaciones.
    """
    user_id = current_user.id
    user_data = _user_causas.get(user_id, {})
    causas_raw = user_data.get('causas', [])

    if causa_id < 1 or causa_id > len(causas_raw):
        raise HTTPException(status_code=404, detail="Causa no encontrada")

    c = causas_raw[causa_id - 1]
    actuaciones = [
        ActuacionResponse(**a) for a in c.get('actuaciones', [])
    ]

    return CausaResponse(
        id=causa_id,
        tipo=c.get('tipo', ''),
        rit=c.get('rit', ''),
        ruc=c.get('ruc', ''),
        tribunal=c.get('tribunal', ''),
        caratulado=c.get('caratulado', ''),
        fecha_ingreso=c.get('fecha_ingreso', ''),
        estado=c.get('estado', ''),
        procedimiento=c.get('procedimiento', ''),
        etapa=c.get('etapa', ''),
        ultima_actuacion=c.get('ultima_actuacion'),
        fecha_ultima_actuacion=c.get('fecha_ultima_actuacion'),
        actuaciones=actuaciones,
        actuaciones_count=len(actuaciones)
    )


@router.delete("/clear")
async def clear_causas(
    current_user: User = Depends(get_current_user)
):
    """
    Elimina las causas sincronizadas del usuario.
    """
    user_id = current_user.id
    if user_id in _user_causas:
        del _user_causas[user_id]

    return {"success": True, "message": "Datos eliminados"}
