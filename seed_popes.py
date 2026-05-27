import json
import os
import re
from datetime import datetime, date
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import Pope

def safe_date_parse(date_str):
    if not date_str:
        return None
        
    clean_str = str(date_str).replace('?', '').replace('.', '-').strip()
    
    try:
        from datetime import datetime, date
        if '-' in clean_str and len(clean_str.split('-')) == 3:
            return datetime.strptime(clean_str, "%Y-%m-%d").date()
            
        if clean_str.isdigit():
            return date(int(clean_str), 1, 1)
            
    except ValueError:
        return None
        
    return None

def standardize_historical_date(date_str):
    if not date_str or str(date_str).strip().lower() in ["present", "-", ""]:
        return None, None

    clean_str = str(date_str).strip().lower()
    modifier = "exact"

    if "c." in clean_str or "circa" in clean_str:
        modifier = "circa"
        clean_str = clean_str.replace("c.", "").replace("circa", "").strip()
    elif "after" in clean_str:
        modifier = "after"
        clean_str = clean_str.replace("after", "").strip()
    elif "before" in clean_str:
        modifier = "before"
        clean_str = clean_str.replace("before", "").strip()

    if '-' in clean_str or '–' in clean_str:
        modifier = "circa"
        clean_str = clean_str.replace('–', '-').split('-')[0].strip()

    if clean_str.isdigit() and len(clean_str) <= 4:
        from datetime import date
        return date(int(clean_str), 1, 1), modifier

    parts = clean_str.split()
    
    try:
        from datetime import datetime
        if len(parts) >= 3:
            if len(parts[1]) == 3:
                parsed_date = datetime.strptime(clean_str, "%d %b %Y")
            else:
                parsed_date = datetime.strptime(clean_str, "%d %B %Y")
            return parsed_date.date(), modifier
            
        elif len(parts) == 2:
            if len(parts[0]) == 3:
                parsed_date = datetime.strptime(clean_str, "%b %Y")
            else:
                parsed_date = datetime.strptime(clean_str, "%B %Y")
            return parsed_date.date(), modifier
            
        else:
            return None, modifier
            
    except ValueError:
        return None, modifier
    except Exception as e:
        print(f"    [!] Critical error converting '{date_str}': {e}")
        return None, modifier

def seed_popes_from_json():
    filepath = os.path.join("data", "popes.json")
    
    if not os.path.exists(filepath):
        print(f"[!] File {filepath} not found. Did you run the spider first?")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        popes_data = json.load(f)

    db: Session = SessionLocal()

    print(f"[*] Starting ETL pipeline for {len(popes_data)} Popes...")
    
    inserted_count = 0
    skipped_count = 0

    try:
        for p_data in popes_data:
            existing_pope = db.query(Pope).filter(
                Pope.succession_number == int(p_data["succession_number"])
            ).first()

            if existing_pope:
                skipped_count += 1
                continue

            start_date, start_mod = standardize_historical_date(p_data.get("pontificate_start"))
            end_date, end_mod = standardize_historical_date(p_data.get("pontificate_end"))

            b_date_str = p_data.get("birth_date")
            parsed_b_date = None
            if b_date_str:
                try:
                    parsed_b_date = datetime.strptime(b_date_str, "%Y-%m-%d").date()
                except ValueError:
                    pass 

            exact_start = safe_date_parse(p_data.get("profile_pontificate_start"))
            exact_end = safe_date_parse(p_data.get("profile_pontificate_end"))
            
            str_start = str(p_data.get("profile_pontificate_start") or "")
            str_end = str(p_data.get("profile_pontificate_end") or "")
            mod_start = "circa" if len(str_start.strip()) <= 4 else "exact"
            mod_end = "circa" if len(str_end.strip()) <= 4 else "exact"

            parsed_elected = safe_date_parse(p_data.get("elected_pontiff_date")) or exact_start

            new_pope = Pope(
                succession_number=int(p_data["succession_number"]),
                papal_name=p_data["papal_name"],
                baptism_name=p_data.get("baptism_name"),
                religious_order=p_data.get("religious_order"),
                
                pontificate_start=exact_start,
                start_date_modifier=mod_start,
                pontificate_end=exact_end,
                end_date_modifier=mod_end,
                
                birth_date=safe_date_parse(p_data.get("birth_date")),
                birth_place=p_data.get("birth_place"),
                episcopal_motto=p_data.get("episcopal_motto"),
                cardinals_created=p_data.get("cardinals_created", 0),
                documents_issued=p_data.get("documents_issued", 0),
                saints_proclaimed=p_data.get("saints_proclaimed", 0),
                blesseds_proclaimed=p_data.get("blesseds_proclaimed", 0),
                
                ordained_priest_date=safe_date_parse(p_data.get("ordained_priest_date")),
                consecrated_bishop_date=safe_date_parse(p_data.get("consecrated_bishop_date")),
                created_cardinal_date=safe_date_parse(p_data.get("created_cardinal_date")),
                
                elected_pontiff_date=parsed_elected, 
                installed_pontiff_date=safe_date_parse(p_data.get("installed_pontiff_date")),
                
                death_date=safe_date_parse(p_data.get("death_date")), 
                death_place=p_data.get("death_place"),
                
                beatified_date=safe_date_parse(p_data.get("beatified_date")),
                canonised_date=safe_date_parse(p_data.get("canonised_date")),
                feast_day=p_data.get("feast_day"),
                buried_at=p_data.get("buried_at")
            )
            
            db.add(new_pope)
            inserted_count += 1

        db.commit()
        print(f"\n=== ETL SUMMARY ===")
        print(f"Total inserted: {inserted_count}")
        print(f"Total skipped (already exist): {skipped_count}")
        print(f"===================")

    except Exception as e:
        db.rollback()
        print(f"[!] Database error during transaction: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_popes_from_json()