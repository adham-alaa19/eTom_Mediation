from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime
from DB.db import SessionLocal

app = FastAPI(title="TMF633_API")

class ValidFor(BaseModel):
    startDateTime: datetime
    endDateTime: Optional[datetime]

class SimpleServiceSpecification(BaseModel):
    id: str
    name: str
    lifecycle_status: str
    validFor: ValidFor



@app.get("/tmf-api/serviceCatalogManagement/v4/serviceSpecification")
def get_all_service_specs(db=Depends(SessionLocal)):
    rows = db.execute(text("""
        SELECT spec_json FROM service_specification
    """)).fetchall()
    return [r[0] for r in rows]



@app.post("/tmf-api/serviceCatalogManagement/v4/serviceSpecification")
def create_service_spec(spec: SimpleServiceSpecification, db=Depends(SessionLocal)):
    db.execute(text("""
        INSERT INTO service_specification (
            id, name, lifecycle_status, valid_for_start, valid_for_end, spec_json
        ) VALUES (
            :id, :name, :status, :start, :end, :json
        )
    """), {
        "id": spec.id,
        "name": spec.name,
        "status": spec.lifecycle_status,
        "start": spec.validFor.startDateTime,
        "end": spec.validFor.endDateTime,
        "json": spec.dict()
    })
    db.commit()
    return {"message": "ServiceSpecification created", "id": spec.id}

@app.get("/tmf-api/serviceCatalogManagement/v4/serviceSpecification/{spec_id}")
def get_service_spec(spec_id: str, db=Depends(SessionLocal)):
    row = db.execute(text("""
        SELECT spec_json FROM service_specification WHERE id = :id
    """), {"id": spec_id}).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Service Specification not found")
    return row[0]

