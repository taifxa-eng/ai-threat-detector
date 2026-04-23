from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from models.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    source_ip = Column(String, nullable=False)
    destination_ip = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    severity = Column(Integer, nullable=False)
    risk_label = Column(String, nullable=False)
    details = Column(String, nullable=False)
    bytes_in = Column(Integer, nullable=False)
    bytes_out = Column(Integer, nullable=False)
    is_anomaly = Column(Boolean, default=False)
