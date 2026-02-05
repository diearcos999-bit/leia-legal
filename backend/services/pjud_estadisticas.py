"""
Servicio para consumir las APIs de Estadísticas del Poder Judicial de Chile.
Base URL: https://estadisticaservices.pjud.cl

Estas APIs proporcionan datos estadísticos públicos agregados,
no información de casos individuales.
"""

import httpx
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from services.pjud_constants import (
    CORTES_APELACIONES,
    COMPETENCIAS,
    get_corte_nombre,
    get_tribunal_nombre,
)

logger = logging.getLogger(__name__)


# ==================== CONFIGURACIÓN ====================

BASE_URL = "https://estadisticaservices.pjud.cl"
TIMEOUT = 30.0  # segundos

# Endpoints disponibles
ENDPOINTS = {
    "ingresos": "/pjen/ingresos_rol_competencia",
    "terminos": "/pjen/terminos_rol_competencia",
    "tramitacion": "/pjen/causas_tramitacion_competencia",
    "duracion": "/pjen/duracion_causas_competencia",
    "audiencias": "/pjen/audiencias_realizadas_competencia",
}


# ==================== DATACLASSES ====================

@dataclass
class EstadisticaIngreso:
    """Estadística de ingresos de causas."""
    año: int
    corte: str
    competencia: str
    total_ingresos: int
    detalle: Dict[str, Any]


@dataclass
class EstadisticaTermino:
    """Estadística de términos de causas."""
    año: int
    corte: str
    competencia: str
    total_terminos: int
    detalle: Dict[str, Any]


@dataclass
class EstadisticaTramitacion:
    """Estadística de causas en tramitación."""
    año: int
    corte: str
    competencia: str
    total_causas: int
    detalle: Dict[str, Any]


@dataclass
class EstadisticaDuracion:
    """Estadística de duración de causas."""
    año: int
    corte: str
    competencia: str
    duracion_promedio_dias: float
    detalle: Dict[str, Any]


@dataclass
class EstadisticaAudiencia:
    """Estadística de audiencias realizadas."""
    año: int
    corte: str
    competencia: str
    total_audiencias: int
    detalle: Dict[str, Any]


# ==================== CLIENTE API ====================

class PJUDEstadisticasClient:
    """
    Cliente para las APIs de Estadísticas del Poder Judicial.
    """

    def __init__(self):
        self.base_url = BASE_URL
        self.client = httpx.AsyncClient(timeout=TIMEOUT)

    async def close(self):
        """Cierra el cliente HTTP."""
        await self.client.aclose()

    async def _request(
        self,
        endpoint: str,
        año: int,
        corte: int = 0,
        competencia: str = "Civil",
        tribunal: Optional[int] = None,
        seccion: str = "0"
    ) -> Dict[str, Any]:
        """
        Realiza una petición a la API de estadísticas.

        Args:
            endpoint: Nombre del endpoint (ver ENDPOINTS)
            año: Año de consulta (desde 2015)
            corte: Código de Corte de Apelaciones (0 = Todo el país)
            competencia: Tipo de competencia (Civil, Familia, Laboral, etc.)
            tribunal: Código de tribunal específico (opcional)
            seccion: Sección (default "0")

        Returns:
            Dict con los datos de la API
        """
        if endpoint not in ENDPOINTS:
            raise ValueError(f"Endpoint '{endpoint}' no válido. Usar: {list(ENDPOINTS.keys())}")

        if año < 2015:
            raise ValueError("El año debe ser 2015 o posterior")

        url = f"{self.base_url}{ENDPOINTS[endpoint]}"

        params = {
            "año": año,
            "corte": corte,
            "competencia": competencia,
            "seccion": seccion,
        }

        if tribunal:
            params["tribunal"] = tribunal

        try:
            logger.info(f"Consultando {url} con params: {params}")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Respuesta exitosa de {endpoint}")
            return {
                "success": True,
                "data": data,
                "params": params,
                "timestamp": datetime.now().isoformat()
            }
        except httpx.HTTPStatusError as e:
            logger.error(f"Error HTTP en {endpoint}: {e.response.status_code}")
            return {
                "success": False,
                "error": f"Error HTTP: {e.response.status_code}",
                "params": params
            }
        except httpx.RequestError as e:
            logger.error(f"Error de conexión en {endpoint}: {e}")
            return {
                "success": False,
                "error": f"Error de conexión: {str(e)}",
                "params": params
            }
        except Exception as e:
            logger.error(f"Error inesperado en {endpoint}: {e}")
            return {
                "success": False,
                "error": str(e),
                "params": params
            }

    # ==================== MÉTODOS PÚBLICOS ====================

    async def get_ingresos(
        self,
        año: int,
        corte: int = 0,
        competencia: str = "Civil",
        tribunal: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas de ingresos de causas.

        Args:
            año: Año de consulta
            corte: Código de corte (0 = todo el país)
            competencia: Tipo de competencia
            tribunal: Código de tribunal específico

        Returns:
            Dict con estadísticas de ingresos
        """
        result = await self._request("ingresos", año, corte, competencia, tribunal)

        if result["success"]:
            result["corte_nombre"] = get_corte_nombre(corte)
            result["competencia_label"] = COMPETENCIAS.get(competencia, competencia)

        return result

    async def get_terminos(
        self,
        año: int,
        corte: int = 0,
        competencia: str = "Civil",
        tribunal: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas de términos de causas.

        Args:
            año: Año de consulta
            corte: Código de corte (0 = todo el país)
            competencia: Tipo de competencia
            tribunal: Código de tribunal específico

        Returns:
            Dict con estadísticas de términos
        """
        result = await self._request("terminos", año, corte, competencia, tribunal)

        if result["success"]:
            result["corte_nombre"] = get_corte_nombre(corte)
            result["competencia_label"] = COMPETENCIAS.get(competencia, competencia)

        return result

    async def get_causas_tramitacion(
        self,
        año: int,
        corte: int = 0,
        competencia: str = "Civil",
        tribunal: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas de causas en tramitación.

        Args:
            año: Año de consulta
            corte: Código de corte (0 = todo el país)
            competencia: Tipo de competencia
            tribunal: Código de tribunal específico

        Returns:
            Dict con estadísticas de tramitación
        """
        result = await self._request("tramitacion", año, corte, competencia, tribunal)

        if result["success"]:
            result["corte_nombre"] = get_corte_nombre(corte)
            result["competencia_label"] = COMPETENCIAS.get(competencia, competencia)

        return result

    async def get_duracion_causas(
        self,
        año: int,
        corte: int = 0,
        competencia: str = "Civil",
        tribunal: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas de duración de causas.

        Args:
            año: Año de consulta
            corte: Código de corte (0 = todo el país)
            competencia: Tipo de competencia
            tribunal: Código de tribunal específico

        Returns:
            Dict con estadísticas de duración
        """
        result = await self._request("duracion", año, corte, competencia, tribunal)

        if result["success"]:
            result["corte_nombre"] = get_corte_nombre(corte)
            result["competencia_label"] = COMPETENCIAS.get(competencia, competencia)

        return result

    async def get_audiencias(
        self,
        año: int,
        corte: int = 0,
        competencia: str = "Civil",
        tribunal: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas de audiencias realizadas.

        Args:
            año: Año de consulta
            corte: Código de corte (0 = todo el país)
            competencia: Tipo de competencia
            tribunal: Código de tribunal específico

        Returns:
            Dict con estadísticas de audiencias
        """
        result = await self._request("audiencias", año, corte, competencia, tribunal)

        if result["success"]:
            result["corte_nombre"] = get_corte_nombre(corte)
            result["competencia_label"] = COMPETENCIAS.get(competencia, competencia)

        return result

    async def get_resumen_anual(
        self,
        año: int,
        corte: int = 0,
        competencia: str = "Civil"
    ) -> Dict[str, Any]:
        """
        Obtiene un resumen completo de estadísticas del año.

        Args:
            año: Año de consulta
            corte: Código de corte
            competencia: Tipo de competencia

        Returns:
            Dict con resumen de todas las estadísticas
        """
        ingresos = await self.get_ingresos(año, corte, competencia)
        terminos = await self.get_terminos(año, corte, competencia)
        tramitacion = await self.get_causas_tramitacion(año, corte, competencia)

        return {
            "año": año,
            "corte": get_corte_nombre(corte),
            "corte_codigo": corte,
            "competencia": competencia,
            "ingresos": ingresos,
            "terminos": terminos,
            "tramitacion": tramitacion,
            "timestamp": datetime.now().isoformat()
        }

    async def get_comparativa_cortes(
        self,
        año: int,
        competencia: str = "Civil"
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas comparativas entre todas las cortes.

        Args:
            año: Año de consulta
            competencia: Tipo de competencia

        Returns:
            Dict con estadísticas por corte
        """
        resultados = {}

        for codigo, nombre in CORTES_APELACIONES.items():
            if codigo == 0:  # Saltar "Todo el país"
                continue

            try:
                ingresos = await self.get_ingresos(año, codigo, competencia)
                resultados[nombre] = {
                    "codigo": codigo,
                    "ingresos": ingresos.get("data") if ingresos.get("success") else None,
                    "error": ingresos.get("error") if not ingresos.get("success") else None
                }
            except Exception as e:
                resultados[nombre] = {
                    "codigo": codigo,
                    "error": str(e)
                }

        return {
            "año": año,
            "competencia": competencia,
            "cortes": resultados,
            "timestamp": datetime.now().isoformat()
        }


# ==================== FUNCIONES DE CONVENIENCIA ====================

async def obtener_estadisticas_rapidas(
    año: int = None,
    corte: int = 90,  # Santiago por defecto
    competencia: str = "Civil"
) -> Dict[str, Any]:
    """
    Función de conveniencia para obtener estadísticas rápidamente.

    Args:
        año: Año de consulta (default: año actual)
        corte: Código de corte (default: Santiago)
        competencia: Tipo de competencia

    Returns:
        Dict con estadísticas básicas
    """
    if año is None:
        año = datetime.now().year - 1  # Año anterior para datos completos

    client = PJUDEstadisticasClient()
    try:
        return await client.get_resumen_anual(año, corte, competencia)
    finally:
        await client.close()


# ==================== DEMO DATA ====================

def get_demo_estadisticas(
    año: int = 2024,
    corte: int = 90,
    competencia: str = "Civil"
) -> Dict[str, Any]:
    """
    Genera datos de demostración para estadísticas.
    Útil cuando la API no está disponible.
    """
    return {
        "success": True,
        "demo_mode": True,
        "año": año,
        "corte": get_corte_nombre(corte),
        "corte_codigo": corte,
        "competencia": competencia,
        "data": {
            "ingresos": {
                "total": 45678,
                "por_materia": {
                    "Cobro de Pesos": 12500,
                    "Indemnización de Perjuicios": 8900,
                    "Juicio Ejecutivo": 15000,
                    "Otros": 9278
                }
            },
            "terminos": {
                "total": 42150,
                "por_forma_termino": {
                    "Sentencia Definitiva": 18500,
                    "Abandono del Procedimiento": 8200,
                    "Avenimiento": 6500,
                    "Otros": 8950
                }
            },
            "tramitacion": {
                "total_activas": 28456,
                "por_estado": {
                    "En Tramitación": 22000,
                    "En Acuerdo": 3200,
                    "Suspendida": 1800,
                    "Paralizada": 1456
                }
            },
            "duracion_promedio_dias": 245,
            "audiencias_realizadas": 38900
        },
        "timestamp": datetime.now().isoformat()
    }
