from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import database
import models
import schemas
import scanner

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Kurumsal DevSecOps API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/scan", response_model=dict)
def scan_image(image_name: str, db: Session = Depends(database.get_db)):
    """
    Scans a docker image using Trivy and saves the result to DB.
    """
    scan_result = scanner.run_trivy_scan(image_name)
    
    # Save to database
    db_record = models.ScanRecord(
        image_name=image_name,
        status=scan_result["status"],
        critical_count=scan_result["counts"].get("CRITICAL", 0),
        high_count=scan_result["counts"].get("HIGH", 0),
        medium_count=scan_result["counts"].get("MEDIUM", 0),
        low_count=scan_result["counts"].get("LOW", 0)
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return {
        "record_id": db_record.id,
        "image_name": image_name,
        "status": scan_result["status"],
        "counts": scan_result["counts"],
        "vulnerabilities": scan_result["vulnerabilities"],
        "is_mock": scan_result.get("is_mock", False),
        "mock_reason": scan_result.get("mock_reason")
    }

@app.get("/api/history", response_model=List[schemas.ScanRecord])
def get_history(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Retrieves past scan records.
    """
    records = db.query(models.ScanRecord).order_by(models.ScanRecord.id.desc()).offset(skip).limit(limit).all()
    return records
