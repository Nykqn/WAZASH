from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    endpoint_id = Column(String, unique=True, index=True, nullable=False)
    hostname = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    os = Column(String, nullable=True)
    status = Column(String, default="active", nullable=False)  # active, inactive, down
    last_seen = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
