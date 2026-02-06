#!/usr/bin/env python3
"""
Script para procesar apuntes legales y subirlos a Pinecone

Procesa PDFs y DOCX, genera embeddings y sube a Pinecone vectorstore.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar dependencias
try:
    import openai
    from pinecone import Pinecone, ServerlessSpec
    import PyPDF2
    from docx import Document
except ImportError as e:
    print(f"❌ Falta instalar dependencias: {e}")
    print("\nInstala con:")
    print("  pip install openai pinecone-client PyPDF2 python-docx")
    exit(1)

# Configuración
APUNTES_DIR = Path("/Users/solangemendez/Downloads/apuntes leia")
INDEX_NAME = "leia-legal"
CHUNK_SIZE = 1000  # caracteres por chunk
CHUNK_OVERLAP = 200  # overlap entre chunks


def extract_text_from_pdf(file_path: Path) -> str:
    """Extrae texto de un PDF"""
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"  ⚠️  Error leyendo PDF {file_path.name}: {e}")
    return text


def extract_text_from_docx(file_path: Path) -> str:
    """Extrae texto de un DOCX"""
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"  ⚠️  Error leyendo DOCX {file_path.name}: {e}")
    return text


def extract_text(file_path: Path) -> str:
    """Extrae texto de PDF o DOCX"""
    suffix = file_path.suffix.lower()
    if suffix == '.pdf':
        return extract_text_from_pdf(file_path)
    elif suffix == '.docx':
        return extract_text_from_docx(file_path)
    else:
        print(f"  ⚠️  Formato no soportado: {suffix}")
        return ""


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Divide texto en chunks con overlap"""
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Intentar cortar en un punto natural (., \n)
        if end < len(text):
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            cut_point = max(last_period, last_newline)
            if cut_point > chunk_size * 0.5:  # Solo si está después de la mitad
                chunk = chunk[:cut_point + 1]
                end = start + cut_point + 1

        chunks.append(chunk.strip())
        start = end - overlap

    return [c for c in chunks if len(c) > 50]  # Filtrar chunks muy pequeños


def generate_embedding(text: str, client) -> List[float]:
    """Genera embedding con OpenAI"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def get_category(filename: str) -> str:
    """Detecta categoría basada en nombre de archivo"""
    name = filename.lower()

    if 'familia' in name or '19947' in name or '19968' in name:
        return 'familia'
    elif 'tributario' in name:
        return 'tributario'
    elif 'penal' in name or 'couso' in name:
        return 'penal'
    elif 'procesal' in name or 'cpc' in name or '1552' in name:
        return 'procesal'
    elif 'constitucional' in name or 'jurisdiccion' in name or 'lovera' in name or 'garantias' in name:
        return 'constitucional'
    elif 'trabajo' in name or 'laboral' in name:
        return 'laboral'
    elif 'sociedades' in name or 'insolvencia' in name or '20720' in name:
        return 'comercial'
    elif 'consumidor' in name or '19496' in name or 'sernac' in name:
        return 'consumidor'
    elif 'codigo' in name or 'cot' in name or 'organico' in name:
        return 'codigos'
    else:
        return 'general'


def main():
    print("=" * 60)
    print("PROCESADOR DE APUNTES PARA LEIA")
    print("=" * 60)

    # Verificar API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    pinecone_key = os.getenv("PINECONE_API_KEY")

    if not openai_key:
        print("❌ OPENAI_API_KEY no configurada en .env")
        return
    if not pinecone_key:
        print("❌ PINECONE_API_KEY no configurada en .env")
        return

    print("✅ API keys configuradas")

    # Inicializar clientes
    openai_client = openai.OpenAI(api_key=openai_key)
    pc = Pinecone(api_key=pinecone_key)

    # Crear o conectar al índice
    existing_indexes = [idx.name for idx in pc.list_indexes()]

    if INDEX_NAME not in existing_indexes:
        print(f"\n📝 Creando índice: {INDEX_NAME}")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,  # OpenAI embedding dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print("✅ Índice creado")
    else:
        print(f"✅ Conectado a índice: {INDEX_NAME}")

    index = pc.Index(INDEX_NAME)

    # Procesar archivos
    files = list(APUNTES_DIR.glob("*.pdf")) + list(APUNTES_DIR.glob("*.docx"))
    print(f"\n📂 Encontrados {len(files)} archivos para procesar")

    all_vectors = []

    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Procesando: {file_path.name}")

        # Extraer texto
        text = extract_text(file_path)
        if not text:
            print("  ⚠️  Sin texto extraído, saltando...")
            continue

        print(f"  📄 {len(text)} caracteres extraídos")

        # Dividir en chunks
        chunks = chunk_text(text)
        print(f"  📦 {len(chunks)} chunks generados")

        # Generar embeddings y preparar vectores
        category = get_category(file_path.name)

        for j, chunk in enumerate(chunks):
            try:
                # Generar embedding
                embedding = generate_embedding(chunk, openai_client)

                # ID único
                chunk_id = hashlib.md5(f"{file_path.name}_{j}".encode()).hexdigest()

                # Metadata
                metadata = {
                    "text": chunk[:1000],  # Límite de Pinecone
                    "source": file_path.name,
                    "category": category,
                    "chunk_number": j,
                    "total_chunks": len(chunks)
                }

                all_vectors.append((chunk_id, embedding, metadata))

            except Exception as e:
                print(f"  ⚠️  Error en chunk {j}: {e}")

        print(f"  ✅ {len(chunks)} embeddings generados - Categoría: {category}")

    # Subir a Pinecone
    print(f"\n📤 Subiendo {len(all_vectors)} vectores a Pinecone...")

    batch_size = 100
    for i in range(0, len(all_vectors), batch_size):
        batch = all_vectors[i:i + batch_size]
        try:
            index.upsert(vectors=batch)
            print(f"  ✅ Batch {i // batch_size + 1}: {len(batch)} vectores")
        except Exception as e:
            print(f"  ❌ Error en batch: {e}")

    # Verificar
    stats = index.describe_index_stats()
    print(f"\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    print(f"✅ Vectores en Pinecone: {stats.total_vector_count}")
    print(f"✅ Archivos procesados: {len(files)}")
    print(f"\n🎉 ¡Listo! Ahora puedes usar el RAG con Claude.")
    print("   Ejecuta: python main_simple.py")


if __name__ == "__main__":
    main()
