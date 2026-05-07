from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, index=True, nullable=False)
    rule_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    status = Column(String, default="open", nullable=False)
    created_at = Column(DateTime, server_default=func.now())
