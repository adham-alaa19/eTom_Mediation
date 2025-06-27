from uuid import uuid4
from datetime import datetime

def convert(record):
    usage_type = record.get("type", "").lower()

    if usage_type == "voice":
        return convert_voice(record)
    elif usage_type == "data":
        return convert_data(record)
    elif usage_type == "sms":
        return convert_sms(record)
    else:
        raise ValueError(f"Unsupported usage type: {usage_type}")

def convert_voice(record):
    base = _base_convert(record, additional=[
        {"name": "partyB", "value": record["party_b"], "valueType": "string"},
        {"name": "duration", "value": int(float(record["amount"])), "valueType": "integer"}
    ])
    return _format_for_tmf727(base)

def convert_data(record):
    base = _base_convert(record, additional=[
        {"name": "volume", "value": int(record["amount"]), "valueType": "integer"},
        {"name": "destinationIp", "value": record.get("party_b", ""), "valueType": "string"}
    ])
    return _format_for_tmf727(base)

def convert_sms(record):
    base = _base_convert(record, additional=[
        {"name": "receiver", "value": record["party_b"], "valueType": "string"},
        {"name": "messageSize", "value": int(record["amount"]), "valueType": "integer"}
    ])
    return _format_for_tmf727(base)

def _base_convert(record, additional=[]):
    usage_date = datetime.strptime(record["start_time"], "%Y-%m-%d %H:%M:%S") if "start_time" in record else datetime.now()
    return {
        "id": str(uuid4()),
        "subscriber_id": record["party_a"],
        "usage_type": record["type"],
        "usage_date": usage_date,
        "status": "RAW",
        "service_id": str(uuid4()),
        "usage_specification_id": str(uuid4()),
        "related_party_id": str(uuid4()),
        "correlated_session_id": str(uuid4()),
        "cost": float(record["cost"]),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "characteristics": additional
    }

def _format_for_tmf727(record):
    return {
        "id": record["id"],
        "subscriberId": record["subscriber_id"],
        "usageType": record["usage_type"],
        "usageDate": record["usage_date"].isoformat(),
        "status": record["status"],
        "serviceId": record["service_id"],
        "usageSpecificationId": record["usage_specification_id"],
        "relatedPartyId": record["related_party_id"],
        "correlatedSessionId": record["correlated_session_id"],
        "cost": record["cost"],
        "characteristics": record["characteristics"]
    }
