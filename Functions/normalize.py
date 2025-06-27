import datetime
import uuid

def normalize(record: dict) -> dict:
    record = normalize_timestamps(record)
    record = normalize_units_and_values(record)
    return record

def normalize_timestamps(record: dict) -> dict:
    raw_timestamp = record.get("usage_date", "")
    if isinstance(raw_timestamp, datetime.datetime):
        # Already normalized
        return record

    raw_timestamp = str(raw_timestamp).strip()

    for fmt in ("%d/%m/%Y", "%d/%m/%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            dt = datetime.datetime.strptime(raw_timestamp, fmt)
            record["usage_date"] = dt
            return record
        except ValueError:
            continue

    try:
        dt = datetime.datetime.fromisoformat(raw_timestamp)
        record["usage_date"] = dt
        return record
    except ValueError:
        pass

    try:
        epoch = int(float(raw_timestamp))
        dt = datetime.datetime.fromtimestamp(epoch)
        record["usage_date"] = dt
        return record
    except (ValueError, OSError):
        pass

    raise ValueError(f"Unknown timestamp format: {raw_timestamp}")

def normalize_units_and_values(record: dict) -> dict:
    if "volume" in record and record["volume"]:
        try:
            record["volume"] = int(float(record["volume"]))
        except ValueError:
            record["volume"] = 0

    if "duration" in record and record["duration"]:
        try:
            record["duration"] = int(float(record["duration"]))
        except ValueError:
            record["duration"] = 0

    if "cost" in record and record["cost"]:
        try:
            record["cost"] = round(float(record["cost"]), 4)  # match DB precision
        except ValueError:
            record["cost"] = 0.0

    return record


