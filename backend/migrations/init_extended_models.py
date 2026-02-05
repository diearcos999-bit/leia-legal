"""
Script para inicializar los modelos extendidos de LEIA.

Ejecutar:
    cd backend
    python migrations/init_extended_models.py
"""

import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, Base

# Importar todos los modelos
from models import User, Conversation, ChatMessage, Feedback, Lawyer, Consultation, PJUDConnection, CausaJudicial
from models_extended import (
    Case, CaseTransfer, CaseDocument, CaseEvent, Consent,
    LawyerService, Review, LawyerMetrics
)


def init_database():
    """Inicializa las tablas en la base de datos"""
    print("🚀 Iniciando creación de tablas...")

    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    print("✅ Tablas creadas exitosamente:")
    for table in Base.metadata.sorted_tables:
        print(f"   - {table.name}")

    print("\n📋 Tablas nuevas del sistema extendido:")
    new_tables = [
        "cases",
        "case_transfers",
        "case_documents",
        "case_events",
        "consents",
        "lawyer_services",
        "reviews",
        "lawyer_metrics"
    ]
    for table in new_tables:
        print(f"   ✓ {table}")


def seed_sample_services():
    """Agrega servicios de ejemplo para abogados existentes"""
    from sqlalchemy.orm import Session
    from database import SessionLocal
    from models_extended import LawyerService, ServiceType

    db = SessionLocal()

    try:
        # Verificar si hay abogados
        lawyers = db.query(Lawyer).limit(5).all()

        if not lawyers:
            print("\n⚠️  No hay abogados en la BD. Omitiendo seed de servicios.")
            return

        print(f"\n🌱 Agregando servicios de ejemplo para {len(lawyers)} abogados...")

        for lawyer in lawyers:
            # Verificar si ya tiene servicios
            existing = db.query(LawyerService).filter(
                LawyerService.lawyer_id == lawyer.id
            ).first()

            if existing:
                print(f"   - {lawyer.name}: ya tiene servicios")
                continue

            # Agregar servicios estándar
            services = [
                LawyerService(
                    lawyer_id=lawyer.id,
                    service_type=ServiceType.INITIAL_CONSULTATION,
                    name="Consulta inicial",
                    description="Primera consulta para evaluar tu caso",
                    price=30000,
                    duration_minutes=30,
                    legal_areas=[lawyer.specialty]
                ),
                LawyerService(
                    lawyer_id=lawyer.id,
                    service_type=ServiceType.HOURLY,
                    name="Hora de asesoría",
                    description="Asesoría legal por hora",
                    price=50000,
                    duration_minutes=60,
                    legal_areas=[lawyer.specialty]
                )
            ]

            for service in services:
                db.add(service)

            print(f"   ✓ {lawyer.name}: 2 servicios agregados")

        db.commit()
        print("✅ Servicios de ejemplo agregados")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    print("=" * 60)
    print("   LEIA - Inicialización de Modelos Extendidos")
    print("=" * 60)
    print()

    init_database()
    seed_sample_services()

    print()
    print("=" * 60)
    print("   ✅ Inicialización completada")
    print("=" * 60)
    print()
    print("Próximos pasos:")
    print("1. Agregar routers a main.py:")
    print("   from routers import cases, lawyers_extended, chat_v2")
    print("   app.include_router(cases.router)")
    print("   app.include_router(lawyers_extended.router)")
    print("   app.include_router(chat_v2.router)")
    print()
    print("2. Reiniciar el servidor:")
    print("   python main.py")
    print()


if __name__ == "__main__":
    main()
