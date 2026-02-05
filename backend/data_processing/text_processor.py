"""
Text Processor - Limpia y prepara textos legales para el RAG system

- Normaliza textos
- Elimina caracteres innecesarios
- Divide en chunks apropiados para embeddings
- Mantiene contexto legal importante
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class TextProcessor:
    """Procesador de textos legales para RAG"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Args:
            chunk_size: Tamaño máximo de cada chunk en caracteres
            chunk_overlap: Solapamiento entre chunks para mantener contexto
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def clean_text(self, text: str) -> str:
        """
        Limpia y normaliza texto legal

        - Elimina espacios múltiples
        - Normaliza saltos de línea
        - Mantiene estructura legal (artículos, numeración)
        """
        # Eliminar espacios múltiples
        text = re.sub(r' +', ' ', text)

        # Normalizar saltos de línea (máximo 2 seguidos)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Eliminar espacios al inicio/final de líneas
        text = '\n'.join(line.strip() for line in text.split('\n'))

        # Eliminar líneas vacías al inicio/final
        text = text.strip()

        return text

    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Divide texto en chunks apropiados para embeddings

        Estrategia:
        1. Intenta dividir por párrafos completos
        2. Si un párrafo es muy largo, divide por oraciones
        3. Mantiene solapamiento para contexto
        """
        text = self.clean_text(text)

        # Dividir por doble salto de línea (párrafos)
        paragraphs = text.split('\n\n')

        chunks = []
        current_chunk = ""
        current_size = 0

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            paragraph_size = len(paragraph)

            # Si el párrafo cabe en el chunk actual
            if current_size + paragraph_size + 2 <= self.chunk_size:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                    current_size += paragraph_size + 2
                else:
                    current_chunk = paragraph
                    current_size = paragraph_size
            else:
                # Guardar chunk actual si tiene contenido
                if current_chunk:
                    chunks.append({
                        "text": current_chunk,
                        "size": current_size,
                        "metadata": metadata.copy()
                    })

                # Si el párrafo es muy grande, dividirlo por oraciones
                if paragraph_size > self.chunk_size:
                    sentences = self._split_sentences(paragraph)
                    temp_chunk = ""
                    temp_size = 0

                    for sentence in sentences:
                        sentence_size = len(sentence)

                        if temp_size + sentence_size + 1 <= self.chunk_size:
                            if temp_chunk:
                                temp_chunk += " " + sentence
                                temp_size += sentence_size + 1
                            else:
                                temp_chunk = sentence
                                temp_size = sentence_size
                        else:
                            if temp_chunk:
                                chunks.append({
                                    "text": temp_chunk,
                                    "size": temp_size,
                                    "metadata": metadata.copy()
                                })
                            temp_chunk = sentence
                            temp_size = sentence_size

                    if temp_chunk:
                        current_chunk = temp_chunk
                        current_size = temp_size
                else:
                    current_chunk = paragraph
                    current_size = paragraph_size

        # Agregar último chunk
        if current_chunk:
            chunks.append({
                "text": current_chunk,
                "size": current_size,
                "metadata": metadata.copy()
            })

        # Agregar IDs y números de chunk
        for idx, chunk in enumerate(chunks):
            chunk["chunk_id"] = f"{metadata.get('source_id', 'unknown')}_{idx}"
            chunk["chunk_number"] = idx + 1
            chunk["total_chunks"] = len(chunks)

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """Divide texto en oraciones"""
        # Patrón para detectar fin de oración
        # Busca punto seguido de espacio y mayúscula, o punto final
        pattern = r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ])|(?<=[.!?])$'

        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]

    def process_law_file(self, input_file: Path) -> List[Dict]:
        """
        Procesa un archivo JSON de ley y genera chunks

        Args:
            input_file: Ruta al archivo JSON de una ley

        Returns:
            Lista de chunks procesados con metadata
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            law_data = json.load(f)

        all_chunks = []

        # Metadata base
        base_metadata = {
            "source": law_data.get("source", "Unknown"),
            "source_id": input_file.stem,
            "law_name": law_data.get("law_name") or law_data.get("title"),
            "category": law_data.get("category"),
            "url": law_data.get("url"),
            "scraped_at": law_data.get("scraped_at"),
            "processed_at": datetime.now().isoformat()
        }

        # Procesar artículos (si existen)
        if "articles" in law_data:
            for article in law_data["articles"]:
                article_text = article.get("content", "")
                article_metadata = base_metadata.copy()
                article_metadata["article_number"] = article.get("article_number")
                article_metadata["type"] = "article"

                chunks = self.chunk_text(article_text, article_metadata)
                all_chunks.extend(chunks)

        # Procesar contenido general (guías, etc.)
        elif "content" in law_data:
            content_text = law_data["content"]
            chunks = self.chunk_text(content_text, base_metadata)
            all_chunks.extend(chunks)

        return all_chunks

    def process_directory(self, input_dir: Path, output_dir: Path) -> Dict:
        """
        Procesa todos los archivos JSON en un directorio

        Args:
            input_dir: Directorio con JSONs de leyes/guías
            output_dir: Directorio donde guardar chunks procesados

        Returns:
            Resumen del procesamiento
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        json_files = list(input_dir.glob("*.json"))
        all_chunks = []

        print(f"\n📂 Procesando {len(json_files)} archivos desde {input_dir}...\n")

        for json_file in json_files:
            print(f"📄 Procesando: {json_file.name}")

            chunks = self.process_law_file(json_file)
            all_chunks.extend(chunks)

            print(f"   ✅ {len(chunks)} chunks generados")

        # Guardar todos los chunks en un archivo
        output_file = output_dir / f"{input_dir.name}_chunks.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Total chunks procesados: {len(all_chunks)}")
        print(f"💾 Guardados en: {output_file}")

        # Resumen
        summary = {
            "total_chunks": len(all_chunks),
            "input_files": len(json_files),
            "output_file": str(output_file),
            "avg_chunk_size": sum(c["size"] for c in all_chunks) / len(all_chunks) if all_chunks else 0,
            "categories": list(set(c["metadata"]["category"] for c in all_chunks if c["metadata"].get("category"))),
            "sources": list(set(c["metadata"]["source"] for c in all_chunks))
        }

        return summary


def main():
    """Script principal para procesar textos legales"""
    print("=" * 60)
    print("TEXT PROCESSOR - JUSTICIAAI")
    print("=" * 60)

    processor = TextProcessor(chunk_size=1000, chunk_overlap=200)

    # Directorios a procesar
    base_dir = Path("data/raw")
    output_dir = Path("data/processed")

    sources = ["bcn", "dt", "sernac"]
    all_summaries = []

    for source in sources:
        source_dir = base_dir / source
        if source_dir.exists():
            print(f"\n{'='*60}")
            print(f"Procesando fuente: {source.upper()}")
            print(f"{'='*60}")

            summary = processor.process_directory(source_dir, output_dir)
            all_summaries.append({"source": source, **summary})
        else:
            print(f"\n⚠️  Directorio no encontrado: {source_dir}")

    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)

    total_chunks = sum(s["total_chunks"] for s in all_summaries)
    print(f"Total chunks generados: {total_chunks}")
    print(f"\nPor fuente:")
    for summary in all_summaries:
        print(f"  • {summary['source'].upper()}: {summary['total_chunks']} chunks")

    print("\n✅ Textos procesados y listos para embeddings!")
    print(f"📂 Ubicación: {output_dir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
