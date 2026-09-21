from pydantic import BaseModel
from datetime import datetime

class ScanRecordBase(BaseModel):
    image_name: str
    status: str
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int

class ScanRecordCreate(ScanRecordBase):
    pass

class ScanRecord(ScanRecordBase):
    id: int
    scan_date: datetime

    class Config:
        from_attributes = True
