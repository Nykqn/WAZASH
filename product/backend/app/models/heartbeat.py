from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class Heartbeat(Base):
    __tablename__ = "heartbeats"
    id = Column(Integer, primary_key=True, index=True)
    endpoint_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
