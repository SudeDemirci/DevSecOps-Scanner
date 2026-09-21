from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, index=True)
    status = Column(String) # PASS, FAIL, ERROR
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    scan_date = Column(DateTime, default=datetime.datetime.utcnow)
