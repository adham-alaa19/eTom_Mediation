import requests
from uuid import uuid4
from datetime import datetime

TMF633_API_URL = "http://localhost:8000/tmf-api/serviceCatalogManagement/v4/serviceSpecification"

def guide(record: dict) -> dict:
    service_name = record.get("serviceName") or record.get("service_name")
    if not service_name:
        record["service_id"] = None
        record.setdefault("usageCharacteristic", []).append({
            "id": str(uuid4()),
            "name": "service_flag",
            "value": "NO_SERVICE_NAME",
            "value_type": "string"
        })
        return record

    try:
        response = requests.get(TMF633_API_URL)
        response.raise_for_status()
        specs = response.json()
    except Exception as e:
        print(f"[guide] API error: {e}")
        record["service_id"] = None
        record.setdefault("usageCharacteristic", []).append({
            "id": str(uuid4()),
            "name": "service_flag",
            "value": "API_ERROR",
            "value_type": "string"
        })
        return record

    now = datetime.utcnow().isoformat()
    matched_id = None
    service_status = None

    for spec in specs:
        name = spec.get("name")
        status = spec.get("lifecycle_status")
        valid_for = spec.get("validFor", {})
        start = valid_for.get("startDateTime")
        end = valid_for.get("endDateTime")

        if name == service_name:
            service_status = status
            if status == "Active" and start <= now and (end is None or end > now):
                matched_id = spec.get("id")
                break

    record["service_id"] = matched_id

    # Set usageCharacteristic flags
    record.setdefault("usageCharacteristic", [])
    record["usageCharacteristic"].append({
        "id": str(uuid4()),
        "name": "service_flag",
        "value": "ACTIVE" if matched_id else "NOT_ACTIVE",
        "value_type": "string"
    })

    return record
