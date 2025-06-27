# In-memory state: last seen records
import datetime
import uuid


last_seen = {}

def correlate(record: dict) -> dict:
    party_a = record.get("subscriber_id")
    party_b = None
    # Check characteristic for "destination_ip", "party_b" or "receiver" depending on usage_type
    usage_type = record.get("usage_type", "").lower()

    # Attempt to find party_b-like info from characteristics or fields
    if usage_type == "data":
        party_b = record.get("destination_ip")
    else:
        party_b = record.get("party_b") or record.get("receiver")

    usage_date = record.get("usage_date")
    if not isinstance(usage_date, datetime.datetime):
        raise ValueError("usage_date must be a datetime object")

    key = (usage_type, party_a, party_b)
    previous = last_seen.get(key)

    if previous:
        delta = abs((usage_date - previous["usage_date"]).total_seconds())
        if delta < 180:  # 3 minutes threshold
            session_id = previous["session_id"]
        else:
            session_id = str(uuid.uuid4())
    else:
        session_id = str(uuid.uuid4())

    record["correlated_session_id"] = session_id
    last_seen[key] = {"usage_date": usage_date, "session_id": session_id}

    # Add/update usage_characteristics list
    if "characteristics" not in record or not isinstance(record["characteristics"], list):
        record["characteristics"] = []

    # Add session_id characteristic, avoid duplicate entries
    if not any(c.get("name") == "session_id" for c in record["characteristics"]):
        record["characteristics"].append({
            "name": "session_id",
            "value": session_id,
            "value_type": "string"
        })

    return record