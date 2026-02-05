"""
Seed script to populate the database with initial lawyer data.
Run this once to populate the lawyers table.

Usage: python seed_lawyers.py
"""
from database import SessionLocal, init_db
from models import Lawyer

# Initial lawyer data (matching the frontend hardcoded data)
LAWYERS_DATA = [
    {
        "name": "María González Pérez",
        "specialty": "Derecho Laboral",
        "experience": "12 años",
        "rating": 4.9,
        "reviews": 127,
        "location": "Santiago Centro",
        "price_min": 50000,
        "price_max": 80000,
        "image": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop",
        "cases": 350,
        "success_rate": 95.0,
        "description": "Especialista en derecho laboral, despidos, finiquitos e indemnizaciones.",
        "is_verified": True
    },
    {
        "name": "Carlos Rodríguez Silva",
        "specialty": "Derecho de Familia",
        "experience": "8 años",
        "rating": 4.8,
        "reviews": 89,
        "location": "Las Condes",
        "price_min": 60000,
        "price_max": 100000,
        "image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop",
        "cases": 210,
        "success_rate": 92.0,
        "description": "Divorcios, pensiones alimenticias, tuición y violencia intrafamiliar.",
        "is_verified": True
    },
    {
        "name": "Ana Martínez Lagos",
        "specialty": "Deudas y Cobranzas",
        "experience": "15 años",
        "rating": 5.0,
        "reviews": 203,
        "location": "Providencia",
        "price_min": 40000,
        "price_max": 70000,
        "image": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop",
        "cases": 520,
        "success_rate": 97.0,
        "description": "Negociación de deudas, DICOM, quiebras y reestructuración financiera.",
        "is_verified": True
    },
    {
        "name": "Jorge Fernández Castro",
        "specialty": "Derecho del Consumidor",
        "experience": "10 años",
        "rating": 4.7,
        "reviews": 156,
        "location": "Ñuñoa",
        "price_min": 45000,
        "price_max": 75000,
        "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop",
        "cases": 280,
        "success_rate": 93.0,
        "description": "SERNAC, productos defectuosos, servicios mal prestados y garantías.",
        "is_verified": True
    },
    {
        "name": "Patricia Soto Ramírez",
        "specialty": "Arriendos",
        "experience": "9 años",
        "rating": 4.9,
        "reviews": 94,
        "location": "Maipú",
        "price_min": 35000,
        "price_max": 60000,
        "image": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=400&h=400&fit=crop",
        "cases": 190,
        "success_rate": 94.0,
        "description": "Contratos de arriendo, desalojos, depósitos de garantía y conflictos.",
        "is_verified": True
    },
    {
        "name": "Ricardo Vargas Muñoz",
        "specialty": "Herencias",
        "experience": "18 años",
        "rating": 4.8,
        "reviews": 175,
        "location": "Santiago Centro",
        "price_min": 70000,
        "price_max": 120000,
        "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop",
        "cases": 410,
        "success_rate": 96.0,
        "description": "Testamentos, posesiones efectivas, partición de bienes y conflictos.",
        "is_verified": True
    }
]


def seed_lawyers():
    """Seed the database with initial lawyer data."""
    # Initialize database tables
    init_db()

    db = SessionLocal()
    try:
        # Check if lawyers already exist
        existing_count = db.query(Lawyer).count()
        if existing_count > 0:
            print(f"⚠️  Ya existen {existing_count} abogados en la base de datos.")
            response = input("¿Deseas agregar más abogados de todos modos? (s/n): ")
            if response.lower() != 's':
                print("Seed cancelado.")
                return

        # Insert lawyers
        for lawyer_data in LAWYERS_DATA:
            lawyer = Lawyer(**lawyer_data)
            db.add(lawyer)

        db.commit()
        print(f"✅ Se insertaron {len(LAWYERS_DATA)} abogados exitosamente.")

        # Show inserted lawyers
        lawyers = db.query(Lawyer).all()
        print("\nAbogados en la base de datos:")
        for lawyer in lawyers:
            print(f"  - {lawyer.id}: {lawyer.name} ({lawyer.specialty})")

    except Exception as e:
        print(f"❌ Error al insertar abogados: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_lawyers()
