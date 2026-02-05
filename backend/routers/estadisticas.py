"""
API endpoints para estadísticas del Poder Judicial y glosario legal.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from services.pjud_estadisticas import (
    PJUDEstadisticasClient,
    get_demo_estadisticas,
)
from services.pjud_constants import (
    CORTES_APELACIONES,
    COMPETENCIAS,
    TODOS_TRIBUNALES,
    get_corte_nombre,
    get_tribunal_nombre,
    extraer_info_rit,
    TIPOS_CAUSA,
    MATERIAS_COMUNES,
)
from services.glosario_legal import (
    buscar_en_todo,
    buscar_terminos_por_categoria,
    obtener_todas_categorias,
    obtener_estadisticas_glosario,
    explicar_para_usuario,
    SIGLAS,
    FRASES_LATINAS,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Estadísticas y Glosario"])

# Modo demo (cambiar a False para usar API real)
DEMO_MODE = True


# ==================== SCHEMAS ====================

class CorteResponse(BaseModel):
    """Información de una Corte de Apelaciones."""
    codigo: int
    nombre: str


class TribunalResponse(BaseModel):
    """Información de un tribunal."""
    codigo: int
    nombre: str


class EstadisticasRequest(BaseModel):
    """Request para consulta de estadísticas."""
    año: int = Field(..., ge=2015, description="Año de consulta (desde 2015)")
    corte: int = Field(default=0, description="Código de corte (0=todo el país)")
    competencia: str = Field(default="Civil", description="Tipo de competencia")


class EstadisticasResponse(BaseModel):
    """Response de estadísticas."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    demo_mode: bool = False
    timestamp: str


class TerminoResponse(BaseModel):
    """Response de búsqueda de término."""
    encontrado: bool
    termino: Optional[str] = None
    tipo: Optional[str] = None
    definicion: Optional[str] = None
    categoria: Optional[str] = None
    sinonimos: Optional[List[str]] = None


class GlosarioStatsResponse(BaseModel):
    """Estadísticas del glosario."""
    total_terminos: int
    total_siglas: int
    total_frases_latinas: int
    categorias: int


class RITInfoResponse(BaseModel):
    """Información extraída de un RIT."""
    rit: str
    tipo: Optional[str]
    numero: Optional[str]
    año: Optional[str]
    competencia: Optional[str]
    descripcion_tipo: Optional[str]


# ==================== ENDPOINTS: CÓDIGOS ====================

@router.get("/cortes", response_model=List[CorteResponse])
async def listar_cortes():
    """
    Lista todas las Cortes de Apelaciones con sus códigos.
    """
    return [
        CorteResponse(codigo=codigo, nombre=nombre)
        for codigo, nombre in CORTES_APELACIONES.items()
    ]


@router.get("/competencias")
async def listar_competencias():
    """
    Lista las competencias disponibles.
    """
    return COMPETENCIAS


@router.get("/tribunales")
async def listar_tribunales(
    competencia: Optional[str] = Query(None, description="Filtrar por competencia")
):
    """
    Lista los tribunales disponibles.
    Opcionalmente filtra por competencia.
    """
    tribunales = [
        TribunalResponse(codigo=codigo, nombre=nombre)
        for codigo, nombre in TODOS_TRIBUNALES.items()
    ]

    if competencia:
        competencia_lower = competencia.lower()
        tribunales = [
            t for t in tribunales
            if competencia_lower in t.nombre.lower()
        ]

    return tribunales


@router.get("/materias/{competencia}")
async def listar_materias(competencia: str):
    """
    Lista las materias comunes de una competencia.
    """
    competencia_lower = competencia.lower()
    if competencia_lower not in MATERIAS_COMUNES:
        raise HTTPException(
            status_code=404,
            detail=f"Competencia '{competencia}' no encontrada. Usar: {list(MATERIAS_COMUNES.keys())}"
        )
    return MATERIAS_COMUNES[competencia_lower]


@router.get("/rit/{rit}", response_model=RITInfoResponse)
async def analizar_rit(rit: str):
    """
    Analiza un RIT y extrae su información.
    Ej: C-1234-2024 -> Civil, número 1234, año 2024
    """
    info = extraer_info_rit(rit)

    descripcion = None
    if info["tipo"]:
        descripcion = TIPOS_CAUSA.get(info["tipo"], "Tipo desconocido")

    return RITInfoResponse(
        rit=rit.upper(),
        tipo=info["tipo"],
        numero=info["numero"],
        año=info["año"],
        competencia=info["competencia"],
        descripcion_tipo=descripcion
    )


# ==================== ENDPOINTS: ESTADÍSTICAS ====================

@router.get("/estadisticas/ingresos", response_model=EstadisticasResponse)
async def get_estadisticas_ingresos(
    año: int = Query(..., ge=2015, description="Año de consulta"),
    corte: int = Query(0, description="Código de corte"),
    competencia: str = Query("Civil", description="Competencia")
):
    """
    Obtiene estadísticas de ingresos de causas del PJUD.
    """
    if DEMO_MODE:
        data = get_demo_estadisticas(año, corte, competencia)
        return EstadisticasResponse(
            success=True,
            data=data["data"]["ingresos"],
            demo_mode=True,
            timestamp=datetime.now().isoformat()
        )

    client = PJUDEstadisticasClient()
    try:
        result = await client.get_ingresos(año, corte, competencia)
        return EstadisticasResponse(
            success=result["success"],
            data=result.get("data"),
            error=result.get("error"),
            demo_mode=False,
            timestamp=datetime.now().isoformat()
        )
    finally:
        await client.close()


@router.get("/estadisticas/resumen", response_model=EstadisticasResponse)
async def get_estadisticas_resumen(
    año: int = Query(..., ge=2015, description="Año de consulta"),
    corte: int = Query(90, description="Código de corte (90=Santiago)"),
    competencia: str = Query("Civil", description="Competencia")
):
    """
    Obtiene un resumen completo de estadísticas del PJUD.
    """
    if DEMO_MODE:
        data = get_demo_estadisticas(año, corte, competencia)
        return EstadisticasResponse(
            success=True,
            data=data["data"],
            demo_mode=True,
            timestamp=datetime.now().isoformat()
        )

    client = PJUDEstadisticasClient()
    try:
        result = await client.get_resumen_anual(año, corte, competencia)
        return EstadisticasResponse(
            success=True,
            data=result,
            demo_mode=False,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        return EstadisticasResponse(
            success=False,
            error=str(e),
            demo_mode=False,
            timestamp=datetime.now().isoformat()
        )
    finally:
        await client.close()


# ==================== ENDPOINTS: GLOSARIO ====================

@router.get("/glosario/buscar", response_model=TerminoResponse)
async def buscar_termino(
    q: str = Query(..., min_length=2, description="Término a buscar")
):
    """
    Busca un término en el glosario legal.
    Busca en términos, siglas y frases latinas.
    """
    resultado = buscar_en_todo(q)

    if not resultado["encontrado"]:
        return TerminoResponse(encontrado=False)

    response = TerminoResponse(
        encontrado=True,
        termino=q,
        tipo=resultado["tipo"],
        definicion=resultado["definicion"]
    )

    if resultado.get("categoria"):
        response.categoria = resultado["categoria"]

    if resultado.get("termino_completo") and resultado["termino_completo"].sinonimos:
        response.sinonimos = resultado["termino_completo"].sinonimos

    return response


@router.get("/glosario/explicar")
async def explicar_termino(
    termino: str = Query(..., min_length=2, description="Término a explicar")
):
    """
    Genera una explicación amigable de un término legal.
    Diseñado para uso con LEIA.
    """
    explicacion = explicar_para_usuario(termino)
    return {
        "termino": termino,
        "explicacion": explicacion
    }


@router.get("/glosario/categorias")
async def listar_categorias():
    """
    Lista todas las categorías del glosario.
    """
    return obtener_todas_categorias()


@router.get("/glosario/categoria/{categoria}")
async def obtener_terminos_categoria(categoria: str):
    """
    Obtiene todos los términos de una categoría específica.
    """
    terminos = buscar_terminos_por_categoria(categoria)

    if not terminos:
        raise HTTPException(
            status_code=404,
            detail=f"Categoría '{categoria}' no encontrada o sin términos"
        )

    return [
        {
            "termino": t.termino,
            "definicion": t.definicion,
            "sinonimos": t.sinonimos
        }
        for t in terminos
    ]


@router.get("/glosario/siglas")
async def listar_siglas():
    """
    Lista todas las siglas legales y sus significados.
    """
    return [
        {"sigla": sigla, "significado": significado}
        for sigla, significado in SIGLAS.items()
    ]


@router.get("/glosario/latinas")
async def listar_frases_latinas():
    """
    Lista todas las frases latinas y sus significados.
    """
    return [
        {"frase": frase, "significado": significado}
        for frase, significado in FRASES_LATINAS.items()
    ]


@router.get("/glosario/stats", response_model=GlosarioStatsResponse)
async def obtener_stats_glosario():
    """
    Obtiene estadísticas del glosario.
    """
    stats = obtener_estadisticas_glosario()
    return GlosarioStatsResponse(**stats)
