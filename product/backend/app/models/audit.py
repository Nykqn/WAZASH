from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())
    action = Column(String, nullable=False)
    user_email = Column(String, nullable=True)
    details = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
