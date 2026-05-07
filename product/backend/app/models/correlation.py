from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base


class CorrelationGroup(Base):
    __tablename__ = "correlation_groups"
    id = Column(Integer, primary_key=True, index=True)
    correlation_type = Column(String, nullable=False, default="ip_repetition")
    source_ip = Column(String, index=True, nullable=False)
    target_ip = Column(String, nullable=True)
    event_type = Column(String, nullable=True)
    window_start = Column(DateTime, nullable=False)
    window_end = Column(DateTime, nullable=False)
    event_count = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
