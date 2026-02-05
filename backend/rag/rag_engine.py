"""
RAG Engine - Sistema de Retrieval-Augmented Generation

Integra búsqueda vectorial con Claude para respuestas legales precisas:
1. Usuario hace pregunta
2. Genera embedding de la pregunta
3. Busca contexto relevante en Pinecone
4. Envía contexto + pregunta a Claude
5. Claude responde usando información verificada
"""

import openai
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

try:
    from rag.vector_store import VectorStore
    VECTOR_STORE_AVAILABLE = True
except ImportError:
    VECTOR_STORE_AVAILABLE = False

load_dotenv()


class RAGEngine:
    """Motor de RAG para respuestas legales precisas"""

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        top_k: int = 3,
        similarity_threshold: float = 0.7
    ):
        """
        Args:
            vector_store: Instancia de VectorStore (Pinecone)
            top_k: Número de documentos relevantes a recuperar
            similarity_threshold: Umbral mínimo de similitud (0-1)
        """
        self.vector_store = vector_store
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

        # Configurar OpenAI para embeddings
        self.openai_key = os.getenv("OPENAI_API_KEY")
        if self.openai_key:
            openai.api_key = self.openai_key

    def generate_query_embedding(self, query: str) -> Optional[List[float]]:
        """
        Genera embedding de la consulta del usuario

        Args:
            query: Pregunta del usuario

        Returns:
            Vector de embeddings
        """
        if not self.openai_key:
            print("⚠️  OpenAI API key no configurada, RAG deshabilitado")
            return None

        try:
            response = openai.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ Error generando embedding de consulta: {e}")
            return None

    def retrieve_context(
        self,
        query: str,
        filter: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Recupera contexto relevante de la base de conocimiento

        Args:
            query: Pregunta del usuario
            filter: Filtros opcionales (ej: {"category": "laboral"})

        Returns:
            Lista de documentos relevantes con scores
        """
        if not self.vector_store:
            print("⚠️  Vector store no inicializado, RAG deshabilitado")
            return []

        # Generar embedding de la consulta
        query_embedding = self.generate_query_embedding(query)
        if not query_embedding:
            return []

        # Buscar documentos similares
        results = self.vector_store.search(
            query_vector=query_embedding,
            top_k=self.top_k,
            filter=filter
        )

        # Filtrar por umbral de similitud
        relevant_docs = [
            doc for doc in results
            if doc["score"] >= self.similarity_threshold
        ]

        return relevant_docs

    def build_context_prompt(self, relevant_docs: List[Dict]) -> str:
        """
        Construye el contexto a inyectar en el prompt de Claude

        Args:
            relevant_docs: Documentos relevantes recuperados

        Returns:
            Texto formateado con el contexto
        """
        if not relevant_docs:
            return ""

        context_parts = ["CONTEXTO LEGAL RELEVANTE:\n"]

        for idx, doc in enumerate(relevant_docs, 1):
            law_name = doc.get("law_name", "Fuente desconocida")
            category = doc.get("category", "general")
            text = doc.get("text", "")
            article = doc.get("article_number")
            url = doc.get("url", "")

            context_parts.append(f"\n[Fuente {idx}]")
            context_parts.append(f"Ley: {law_name}")
            if article:
                context_parts.append(f"Artículo: {article}")
            context_parts.append(f"Categoría: {category}")
            context_parts.append(f"\nContenido:")
            context_parts.append(text)
            if url:
                context_parts.append(f"URL: {url}")
            context_parts.append("-" * 60)

        return "\n".join(context_parts)

    def generate_response(
        self,
        user_query: str,
        conversation_history: List[Dict],
        client,
        system_prompt: str
    ) -> Dict:
        """
        Genera respuesta usando RAG + Claude

        Args:
            user_query: Pregunta del usuario
            conversation_history: Historial de conversación
            client: Cliente de Anthropic (Claude)
            system_prompt: Prompt del sistema base

        Returns:
            Dict con respuesta, fuentes, y metadata
        """
        # 1. Recuperar contexto relevante
        relevant_docs = self.retrieve_context(user_query)

        # 2. Construir contexto
        context = self.build_context_prompt(relevant_docs)

        # 3. Modificar system prompt si hay contexto
        enhanced_system_prompt = system_prompt

        if context:
            enhanced_system_prompt = f"""{system_prompt}

{context}

INSTRUCCIONES ESPECIALES:
- USA la información del CONTEXTO LEGAL RELEVANTE proporcionado arriba para responder con precisión
- CITA las fuentes específicas cuando uses información del contexto (ej: "Según el Código del Trabajo, Artículo X...")
- Si el contexto no cubre completamente la pregunta, indícalo claramente
- SIEMPRE prioriza la información del contexto sobre tu conocimiento general
- Si hay contradicciones, usa el contexto como fuente de verdad
"""

        # 4. Construir mensajes
        messages = []

        # Agregar historial previo
        for msg in conversation_history:
            if isinstance(msg, dict) and msg.get("role") in ['user', 'assistant']:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Agregar consulta actual
        messages.append({
            "role": "user",
            "content": user_query
        })

        # 5. Llamar a Claude
        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                system=enhanced_system_prompt,
                messages=messages
            )

            assistant_message = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens

            # 6. Preparar respuesta con metadata
            return {
                "response": assistant_message,
                "tokens_used": tokens_used,
                "rag_enabled": bool(relevant_docs),
                "sources_used": len(relevant_docs),
                "sources": [
                    {
                        "law_name": doc.get("law_name"),
                        "article": doc.get("article_number"),
                        "category": doc.get("category"),
                        "url": doc.get("url"),
                        "similarity": doc.get("score")
                    }
                    for doc in relevant_docs
                ]
            }

        except Exception as e:
            raise Exception(f"Error generando respuesta RAG: {e}")


def create_rag_engine() -> Optional[RAGEngine]:
    """
    Factory function para crear RAG engine

    Returns:
        RAGEngine si está configurado, None en caso contrario
    """
    # Verificar si RAG está disponible
    if not VECTOR_STORE_AVAILABLE:
        print("ℹ️  Vector Store no disponible, RAG deshabilitado")
        return None

    if not os.getenv("PINECONE_API_KEY"):
        print("ℹ️  Pinecone no configurado, RAG deshabilitado")
        return None

    if not os.getenv("OPENAI_API_KEY"):
        print("ℹ️  OpenAI no configurado, RAG deshabilitado")
        return None

    try:
        # Inicializar vector store
        vector_store = VectorStore()

        # Crear RAG engine
        rag_engine = RAGEngine(
            vector_store=vector_store,
            top_k=3,
            similarity_threshold=0.7
        )

        print("✅ RAG Engine inicializado correctamente")
        return rag_engine

    except Exception as e:
        print(f"⚠️  Error inicializando RAG Engine: {e}")
        print("   Chatbot funcionará sin RAG (solo Claude)")
        return None
