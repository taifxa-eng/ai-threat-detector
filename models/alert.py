from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from models.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    # 🔗 ربط اختياري
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)

    # 📌 بيانات التنبيه الأساسية
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)

    # 🌐 بيانات الشبكة
    ip = Column(String, nullable=True, index=True)
    behavior = Column(String, nullable=True)
    packets = Column(Integer, nullable=True)

    # 🎯 نتائج التحليل
    result = Column(String, nullable=True)   # SAFE / SUSPICIOUS / MALICIOUS
    score = Column(Integer, nullable=True)

    # 🧠 ذكاء إضافي (مهم لكن مو إجباري)
    risk_score = Column(Float, nullable=True)
    severity_level = Column(String, nullable=True)

    # ⚙️ الحالة
    resolved = Column(Boolean, default=False)

    # 🕒 وقت الإنشاء
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)