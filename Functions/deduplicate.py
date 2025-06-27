import hashlib
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from DB.db import SessionLocal

def duplicate(record_data) -> bool:
    char_strings = []
    characteristics = record_data.get("usage_characteristics", [])

    if isinstance(characteristics, list):
        valid_char_items_for_sorting = [
            item for item in characteristics if isinstance(item, dict) and "name" in item
        ]
        sorted_chars = sorted(valid_char_items_for_sorting, key=lambda c: c.get("name", ""))
        for char_dict in sorted_chars:
            name = char_dict.get("name", "")
            value = str(char_dict.get("value", ""))
            char_strings.append(f"{name}:{value}")

    char_concat = ";".join(char_strings)

    usage_date_obj = record_data.get("usage_date")
    if not isinstance(usage_date_obj, datetime):
        raise TypeError(f"Expected 'usage_date' to be a datetime object, got {type(usage_date_obj)}")
    usage_date_str = usage_date_obj.isoformat()

    subscriber_id = record_data.get("subscriber_id", "")
    usage_type = record_data.get("usage_type", "")

    unique_string = f"{subscriber_id}-{usage_type}-{usage_date_str}-{char_concat}"
    record_hash = hashlib.sha256(unique_string.encode("utf-8")).hexdigest()

    session = SessionLocal()
    try:
        session.execute(
            "INSERT INTO deduplication_hash (hash, created_at) VALUES (:hash, NOW())", # type: ignore
            {"hash": record_hash},
        ) # type: ignore
        session.commit()
        return False  # Not a duplicate
    except IntegrityError:
        session.rollback()
        return True  # Duplicate found
    finally:
        session.close()
