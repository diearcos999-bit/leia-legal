"""
Script para crear abogados de prueba en la base de datos.
"""

from database import SessionLocal, engine
from models import Base, Lawyer

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Datos de abogados de prueba
LAWYERS_DATA = [
    # Derecho Civil
    {
        "name": "Carolina Méndez Soto",
        "specialty": "Derecho Civil",
        "experience": "12 años",
        "rating": 4.9,
        "reviews": 127,
        "location": "Providencia, Santiago",
        "price_min": 50000,
        "price_max": 120000,
        "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&h=150&fit=crop&crop=face",
        "cases": 340,
        "success_rate": 0.92,
        "description": "Especialista en contratos, arriendos y cobranzas. Magíster en Derecho Privado UC.",
        "phone": "+56 9 8765 4321",
        "is_verified": True
    },
    {
        "name": "Roberto Fuentes Valdés",
        "specialty": "Derecho Civil",
        "experience": "8 años",
        "rating": 4.7,
        "reviews": 89,
        "location": "Las Condes, Santiago",
        "price_min": 60000,
        "price_max": 150000,
        "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
        "cases": 215,
        "success_rate": 0.88,
        "description": "Experto en derecho inmobiliario y sucesiones. Universidad de Chile.",
        "phone": "+56 9 7654 3210",
        "is_verified": True
    },

    # Derecho Laboral
    {
        "name": "María José Contreras",
        "specialty": "Derecho Laboral",
        "experience": "15 años",
        "rating": 4.8,
        "reviews": 203,
        "location": "Santiago Centro",
        "price_min": 45000,
        "price_max": 100000,
        "image": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150&h=150&fit=crop&crop=face",
        "cases": 520,
        "success_rate": 0.94,
        "description": "Defensora de trabajadores. Ex fiscalizadora de la Dirección del Trabajo.",
        "phone": "+56 9 6543 2109",
        "is_verified": True
    },
    {
        "name": "Andrés Sepúlveda Lagos",
        "specialty": "Derecho Laboral",
        "experience": "10 años",
        "rating": 4.6,
        "reviews": 156,
        "location": "Ñuñoa, Santiago",
        "price_min": 40000,
        "price_max": 90000,
        "image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
        "cases": 380,
        "success_rate": 0.89,
        "description": "Especialista en despidos injustificados y tutela laboral.",
        "phone": "+56 9 5432 1098",
        "is_verified": True
    },

    # Derecho de Familia
    {
        "name": "Francisca Rojas Pizarro",
        "specialty": "Derecho de Familia",
        "experience": "18 años",
        "rating": 4.9,
        "reviews": 312,
        "location": "Vitacura, Santiago",
        "price_min": 70000,
        "price_max": 180000,
        "image": "https://images.unsplash.com/photo-1594744803329-e58b31de8bf5?w=150&h=150&fit=crop&crop=face",
        "cases": 680,
        "success_rate": 0.91,
        "description": "Mediadora familiar certificada. Experta en custodia y pensiones alimenticias.",
        "phone": "+56 9 4321 0987",
        "is_verified": True
    },
    {
        "name": "Gonzalo Herrera Muñoz",
        "specialty": "Derecho de Familia",
        "experience": "7 años",
        "rating": 4.5,
        "reviews": 78,
        "location": "La Florida, Santiago",
        "price_min": 35000,
        "price_max": 80000,
        "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
        "cases": 145,
        "success_rate": 0.85,
        "description": "Divorcios, régimen de visitas y adopciones. Atención cercana.",
        "phone": "+56 9 3210 9876",
        "is_verified": True
    },

    # Derecho Penal
    {
        "name": "Sebastián Morales Bravo",
        "specialty": "Derecho Penal",
        "experience": "20 años",
        "rating": 4.8,
        "reviews": 245,
        "location": "Santiago Centro",
        "price_min": 80000,
        "price_max": 250000,
        "image": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&h=150&fit=crop&crop=face",
        "cases": 890,
        "success_rate": 0.87,
        "description": "Ex defensor penal público. Especialista en delitos económicos.",
        "phone": "+56 9 2109 8765",
        "is_verified": True
    },
    {
        "name": "Valentina Castro Núñez",
        "specialty": "Derecho Penal",
        "experience": "9 años",
        "rating": 4.7,
        "reviews": 134,
        "location": "Providencia, Santiago",
        "price_min": 60000,
        "price_max": 180000,
        "image": "https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=150&h=150&fit=crop&crop=face",
        "cases": 267,
        "success_rate": 0.90,
        "description": "Defensora en casos de VIF y delitos sexuales. Enfoque en víctimas.",
        "phone": "+56 9 1098 7654",
        "is_verified": True
    },

    # Derecho del Consumidor
    {
        "name": "Camila Vega Astudillo",
        "specialty": "Derecho del Consumidor",
        "experience": "6 años",
        "rating": 4.6,
        "reviews": 98,
        "location": "Las Condes, Santiago",
        "price_min": 30000,
        "price_max": 70000,
        "image": "https://images.unsplash.com/photo-1598550874175-4d0ef436c909?w=150&h=150&fit=crop&crop=face",
        "cases": 180,
        "success_rate": 0.93,
        "description": "Reclamos SERNAC, garantías y publicidad engañosa.",
        "phone": "+56 9 0987 6543",
        "is_verified": True
    },
    {
        "name": "Diego Ramírez Saavedra",
        "specialty": "Derecho del Consumidor",
        "experience": "5 años",
        "rating": 4.4,
        "reviews": 67,
        "location": "Maipú, Santiago",
        "price_min": 25000,
        "price_max": 60000,
        "image": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&h=150&fit=crop&crop=face",
        "cases": 120,
        "success_rate": 0.88,
        "description": "Demandas colectivas y defensa ante retail. Precios accesibles.",
        "phone": "+56 9 9876 5432",
        "is_verified": True
    },
]


def seed_lawyers():
    """Poblar la base de datos con abogados de prueba."""
    db = SessionLocal()

    try:
        # Eliminar abogados existentes
        existing = db.query(Lawyer).count()
        if existing > 0:
            db.query(Lawyer).delete()
            db.commit()
            print(f"Eliminados {existing} abogados existentes.")

        # Crear nuevos abogados
        for lawyer_data in LAWYERS_DATA:
            lawyer = Lawyer(**lawyer_data)
            db.add(lawyer)

        db.commit()
        print(f"✅ {len(LAWYERS_DATA)} abogados creados exitosamente!")

        # Mostrar resumen
        print("\nAbogados creados:")
        print("-" * 60)
        for l in LAWYERS_DATA:
            print(f"  • {l['name']} - {l['specialty']} - ⭐ {l['rating']}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_lawyers()
