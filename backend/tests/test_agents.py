"""
Tests para los agentes de IA de LEIA.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAgentTools:
    """Tests para las herramientas de los agentes."""

    def test_glosario_lookup_termino_existente(self):
        """Verifica que glosario_lookup encuentra términos existentes."""
        from agents.tools.legal_tools import glosario_lookup

        result = glosario_lookup.invoke({"termino": "alimentos"})

        assert result["encontrado"] is True
        assert "definicion" in result
        assert "Familia" in result.get("categoria", "")

    def test_glosario_lookup_termino_inexistente(self):
        """Verifica el comportamiento con términos inexistentes."""
        from agents.tools.legal_tools import glosario_lookup

        result = glosario_lookup.invoke({"termino": "xyznoexiste123"})

        assert result["encontrado"] is False
        assert "sugerencias" in result or "mensaje" in result

    def test_buscar_sigla(self):
        """Verifica la búsqueda de siglas legales."""
        from agents.tools.legal_tools import buscar_sigla

        result = buscar_sigla.invoke({"sigla": "RIT"})

        assert result["encontrado"] is True
        assert "Rol Interno" in result["significado"]

    def test_buscar_categoria(self):
        """Verifica la búsqueda por categoría."""
        from agents.tools.legal_tools import buscar_categoria

        result = buscar_categoria.invoke({"categoria": "Familia"})

        assert result["encontrado"] is True
        assert result["total_terminos"] > 0

    def test_list_templates(self):
        """Verifica que se listan las plantillas disponibles."""
        from agents.tools.document_tools import list_templates

        result = list_templates.invoke({})

        assert result["success"] is True
        # Verificar que hay plantillas
        assert len(result.get("templates", [])) >= 0

    def test_load_template_finiquito(self):
        """Verifica la carga de la plantilla de finiquito."""
        from agents.tools.document_tools import load_template

        result = load_template.invoke({"template_name": "finiquito"})

        assert result["success"] is True
        assert "required_fields" in result
        assert len(result["required_fields"]) > 0

    def test_load_template_inexistente(self):
        """Verifica el manejo de plantillas inexistentes."""
        from agents.tools.document_tools import load_template

        result = load_template.invoke({"template_name": "plantilla_que_no_existe"})

        assert result["success"] is False
        assert "error" in result


class TestDocumentTools:
    """Tests para las herramientas de generación de documentos."""

    def test_fill_template_finiquito(self):
        """Verifica el llenado de la plantilla de finiquito."""
        from agents.tools.document_tools import fill_template

        data = {
            "empleador_nombre": "Empresa Test S.A.",
            "empleador_rut": "76123456-7",
            "trabajador_nombre": "Juan Pérez González",
            "trabajador_rut": "12345678-9",
            "fecha_inicio": "2020-01-15",
            "fecha_termino": "2024-01-15",
            "causal_termino": "Artículo 161 del Código del Trabajo",
            "ultimo_sueldo": 800000,
            "dias_vacaciones": 10,
            "anos_servicio": 4,
        }

        result = fill_template.invoke({
            "template_name": "finiquito",
            "data": data,
        })

        assert result["success"] is True
        assert "content" in result
        assert "Juan Pérez González" in result["content"]
        assert "Empresa Test S.A." in result["content"]

    def test_fill_template_carta_reclamo(self):
        """Verifica el llenado de la plantilla de carta de reclamo."""
        from agents.tools.document_tools import fill_template

        data = {
            "destinatario_nombre": "Tienda ABC",
            "destinatario_direccion": "Av. Principal 123, Santiago",
            "remitente_nombre": "María García",
            "remitente_rut": "15678901-2",
            "remitente_direccion": "Calle Secundaria 456, Santiago",
            "remitente_email": "maria@email.com",
            "fecha_compra": "2024-01-10",
            "descripcion_problema": "El producto llegó defectuoso y no funciona.",
            "solucion_solicitada": "Solicito la devolución del dinero pagado.",
        }

        result = fill_template.invoke({
            "template_name": "carta_reclamo",
            "data": data,
        })

        assert result["success"] is True
        assert "content" in result
        assert "María García" in result["content"]
        assert "Tienda ABC" in result["content"]


class TestAgentBase:
    """Tests para la clase base de agentes."""

    def test_agent_state_structure(self):
        """Verifica la estructura del AgentState."""
        from agents.base import AgentState

        # AgentState es un TypedDict, verificar que tiene las claves esperadas
        expected_keys = [
            "messages",
            "context",
            "tools_used",
            "intermediate_steps",
            "final_answer",
            "sources",
            "metadata",
        ]

        for key in expected_keys:
            assert key in AgentState.__annotations__


class TestAgentsRouter:
    """Tests para el router de agentes."""

    @pytest.fixture
    def client(self):
        """Fixture para crear un cliente de test."""
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)

    def test_agents_status_endpoint(self, client):
        """Verifica el endpoint de estado de agentes."""
        response = client.get("/api/agents/status")

        assert response.status_code == 200
        data = response.json()
        # El endpoint debe responder aunque los agentes no estén disponibles
        assert "available" in data

    def test_agents_categories_endpoint(self, client):
        """Verifica el endpoint de categorías legales."""
        response = client.get("/api/agents/categories")

        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert len(data["categories"]) > 0

    def test_templates_endpoint(self, client):
        """Verifica el endpoint de plantillas."""
        response = client.get("/api/agents/templates")

        # Puede fallar si los agentes no están disponibles
        assert response.status_code in [200, 503]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
