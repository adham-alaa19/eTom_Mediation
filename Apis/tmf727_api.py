from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from uuid import uuid4
from datetime import datetime
from DB.db import SessionLocal

app = FastAPI(title="TMF727_API")

class UsageCharacteristic(BaseModel):
    name: str
    value: str
    value_type: str

class UsageSpecification(BaseModel):
    id: str

class RelatedParty(BaseModel):
    id: str

class ServiceUsageRecord(BaseModel):
    subscriber_id: str
    usage_type: str
    usage_date: datetime
    service_id: str
    usageSpecification: UsageSpecification
    relatedParty: list[RelatedParty]
    usageCharacteristic: list[UsageCharacteristic]
    cost: float = 0.0

class Spec(BaseModel):
    id: str
    name: str
    version: str
    lifecycle_status: str
    is_bundle: bool
    specCharacteristic: list

@app.post("/tmf-api/serviceUsageManagement/v5/serviceUsage")
def post_service_usage(record: ServiceUsageRecord, db=Depends(SessionLocal)):
    usage_id = uuid4()
    party_id = uuid4()

    db.execute(text("""
        INSERT INTO related_party (id, name, role, party_type)
        VALUES (:id, :name, 'Customer', 'Individual')
    """), {"id": party_id, "name": record.relatedParty[0].id})

    db.execute(text("""
        INSERT INTO service_usage_record (
            id, subscriber_id, usage_type, usage_date,
            service_id, usage_specification_id, related_party_id,
            cost, status
        )
        VALUES (
            :id, :subscriber_id, :usage_type, :usage_date,
            :service_id, :spec_id, :party_id, :cost, 'processed'
        )
    """), {
        "id": usage_id, "subscriber_id": record.subscriber_id,
        "usage_type": record.usage_type, "usage_date": record.usage_date,
        "service_id": record.service_id,
        "spec_id": record.usageSpecification.id, "party_id": party_id,
        "cost": record.cost
    })

    for char in record.usageCharacteristic:
        db.execute(text("""
            INSERT INTO usage_characteristic (
                id, usage_record_id, name, value, value_type
            ) VALUES (:id, :record_id, :name, :value, :type)
        """), {
            "id": uuid4(), "record_id": usage_id,
            "name": char.name, "value": char.value, "type": char.value_type
        })

    db.commit()
    return {"message": "Service usage recorded", "id": str(usage_id)}

@app.post("/tmf-api/serviceUsageManagement/v5/serviceUsageSpecification")
def create_spec(spec: Spec, db=Depends(SessionLocal)):
    db.execute(text("""
        INSERT INTO service_usage_specification (
            id, name, version, lifecycle_status, is_bundle, spec_json
        ) VALUES (
            :id, :name, :version, :status, :bundle, :json
        )
    """), {
        "id": spec.id, "name": spec.name, "version": spec.version,
        "status": spec.lifecycle_status, "bundle": spec.is_bundle,
        "json": spec.dict()
    })
    db.commit()
    return {"message": "Spec stored", "id": spec.id}

@app.get("/tmf-api/serviceUsageManagement/v5/serviceUsageSpecification/{spec_id}")
def get_spec(spec_id: str, db=Depends(SessionLocal)):
    row = db.execute(text("""
        SELECT spec_json FROM service_usage_specification WHERE id = :id
    """), {"id": spec_id}).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Spec not found")
    return row[0]
