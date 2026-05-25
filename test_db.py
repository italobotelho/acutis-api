import os
import sys
from datetime import date

# Ensure python can find the 'api' module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal
from api.models import Pope, Saint

def run_smoke_test():
    """
    Tests the database connection by inserting one Saint and one Pope.
    """
    db = SessionLocal()

    try:
        # 1. Create Blessed Carlo Acutis
        carlo = Saint(
            official_name="Blessed Carlo Acutis",
            baptism_name="Carlo Acutis",
            gender="M",
            current_status="Blessed",
            feast_day=12,
            feast_month=10,
            birth_date=date(1991, 5, 3),
            short_bio="Italian teenager and amateur computer programmer, best known for documenting Eucharistic miracles."
        )
        
        db.add(carlo)
        db.commit()
        db.refresh(carlo)
        print(f"[*] Success: Inserted Saint -> {carlo.official_name} (ID: {carlo.id})")

        # 2. Create Pope Francis
        francis = Pope(
            succession_number=266,
            papal_name="Francis",
            baptism_name="Jorge Mario Bergoglio",
            nationality="Argentine",
            religious_order="Society of Jesus",
            pontificate_start=date(2013, 3, 13)
        )

        db.add(francis)
        db.commit()
        db.refresh(francis)
        print(f"[*] Success: Inserted Pope -> {francis.papal_name} (ID: {francis.id})")

    except Exception as e:
        db.rollback()
        print(f"[!] Database error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database smoke test...")
    run_smoke_test()