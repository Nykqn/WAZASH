from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    endpoint_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    details = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())
