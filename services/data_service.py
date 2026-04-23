import asyncio
import logging
import random
from datetime import datetime
import pytz
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from ai_engine.anomaly import EVENT_TYPE_MAP, is_anomaly
from models.alert import Alert
from models.base import SessionLocal
from models.event import Event

logger = logging.getLogger("data_service")

EVENT_PATTERNS = [
    {
        "event_type": "DDoS",
        "severity": 9,
        "risk_label": "Critical",
        "details": "Massive traffic spike detected from multiple source IP ranges.",
    },
    {
        "event_type": "Phishing",
        "severity": 7,
        "risk_label": "High",
        "details": "Suspicious email payload and credential harvesting signature.",
    },
    {
        "event_type": "Malware",
        "severity": 8,
        "risk_label": "High",
        "details": "Malicious binary detected in outbound process behavior.",
    },
    {
        "event_type": "SQL Injection",
        "severity": 8,
        "risk_label": "High",
        "details": "Injection payload found in login request parameters.",
    },
    {
        "event_type": "Brute Force",
        "severity": 7,
        "risk_label": "Medium",
        "details": "Repeated login failures from an external IP address.",
    },
    {
        "event_type": "Port Scan",
        "severity": 6,
        "risk_label": "Medium",
        "details": "Recon activity detected from suspicious host range.",
    },
    {
        "event_type": "Ransomware",
        "severity": 10,
        "risk_label": "Critical",
        "details": "Rapid file encryption behavior detected on endpoint.",
    },
]

SOURCE_IP_RANGES = [
    "192.168.64.",
    "10.0.1.",
    "172.16.8.",
    "104.248.22.",
    "45.55.33.",
]


def build_source_ip():
    prefix = random.choice(SOURCE_IP_RANGES)
    return f"{prefix}{random.randint(2, 254)}"


def build_destination_ip():
    return f"10.10.10.{random.randint(10, 240)}"


def create_event(db: Session):
    pattern = random.choice(EVENT_PATTERNS)
    event = Event(
        source_ip=build_source_ip(),
        destination_ip=build_destination_ip(),
        event_type=pattern["event_type"],
        severity=pattern["severity"],
        risk_label=pattern["risk_label"],
        details=pattern["details"],
        bytes_in=random.randint(1200, 25000),
        bytes_out=random.randint(300, 20000),
    )

    recent_events = db.query(Event).order_by(Event.timestamp.desc()).limit(120).all()
    candidate = [
        EVENT_TYPE_MAP.get(pattern["event_type"], 5),
        pattern["severity"],
        event.bytes_in,
        event.bytes_out,
    ]
    event.is_anomaly = is_anomaly(candidate, recent_events)
    db.add(event)
    db.commit()
    db.refresh(event)
    if event.is_anomaly or event.severity >= 8:
        create_alert(db, event)
    return event


def create_alert(db: Session, event: Event):
    severity = (
        "Critical" if event.severity >= 9 else
        "High" if event.severity >= 7 else
        "Medium" if event.severity >= 5 else
        "Low"
    )

    message = f"{event.event_type} detected from {event.source_ip}"

    alert = Alert(
        event_id=event.id,
        title=message,
        description=event.details,

        # 🧠 بيانات ذكية جديدة
        ip=event.source_ip,
        behavior=event.event_type,
        packets=(event.bytes_in + event.bytes_out),

        result="MALICIOUS" if event.severity >= 8 else "SUSPICIOUS",
        score=int(event.severity * 10),

        risk_score=float(event.severity) * 10.0,
        severity_level=severity,
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def get_summary(db: Session):
    rows = db.query(Event.bytes_in, Event.bytes_out).all()
    total_bytes = sum([incoming + outgoing for incoming, outgoing in rows])
    threat_count = db.query(Event).count()
    active_alerts = db.query(Alert).filter(Alert.resolved.is_(False)).count()
    recent_status = "Stable" if threat_count < 30 else "Elevated" if threat_count < 80 else "Critical"
    return {
        "totalTraffic": total_bytes,
        "threatCount": threat_count,
        "alerts": active_alerts,
        "status": recent_status,
    }


def get_recent_alerts(db: Session, limit: int = 10):
    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "ip": a.ip,
            "behavior": a.behavior,
            "packets": a.packets,
            "result": a.result,
            "score": a.score,
            "riskScore": a.risk_score,
            "severity": a.severity_level,
            "createdAt": a.created_at.isoformat(),
            "resolved": a.resolved,
        }
        for a in alerts
    ]


def get_traffic_history(db: Session):
    events = db.query(Event).order_by(Event.timestamp.desc()).limit(18).all()[::-1]
    return [
        {
            "timestamp": event.timestamp.isoformat(),
            "bytes": event.bytes_in + event.bytes_out,
            "type": event.event_type,
        }
        for event in events
    ]


def get_attack_breakdown(db: Session):
    rows = (
        db.query(Event.event_type, func.count(Event.id).label("count"))
        .group_by(Event.event_type)
        .all()
    )
    return [{"label": row[0], "count": row[1]} for row in rows]


def get_suspicious_ips(db: Session):
    rows = (
        db.query(Event.source_ip, func.count(Event.id).label("count"))
        .group_by(Event.source_ip)
        .order_by(func.count(Event.id).desc())
        .limit(8)
        .all()
    )
    return [{"ip": row[0], "events": row[1]} for row in rows]


async def start_data_generation():
    while True:
        try:
            db = SessionLocal()
            create_event(db)
        except Exception as exc:
            logger.error(f"Data generator failed: {exc}")
        finally:
            db.close()
        await asyncio.sleep(4)

def ai_threat_score(packets, behavior):
    base = packets / 1000

    if behavior == "DDoS":
        return min(100, base * 2)
    if behavior == "Ransomware":
        return 100
    if behavior == "SQL Injection":
        return 80
    return 50




async def start_data_generation():
    while True:
        try:
            db: Session = SessionLocal()

            # 🔥 بيانات قليلة
            if random.random() < 0.4:  # يولد أحياناً فقط
                ip = f"192.168.1.{random.randint(1, 255)}"
                behavior = random.choice(["normal", "ddos", "scan"])
                packets = random.randint(100, 1200)

                score = 0
                result = "SAFE"

                if packets > 900:
                    score += 50
                if behavior == "ddos":
                    score += 40

                if score >= 80:
                    result = "MALICIOUS"
                elif score >= 50:
                    result = "SUSPICIOUS"

                db.add(Alert(
                    ip=ip,
                    behavior=behavior,
                    packets=packets,
                    result=result,
                    score=score,
                    created_at=datetime.now(pytz.timezone("Asia/Riyadh"))
                ))

                db.commit()
                print("✔ Light data generated")

            db.close()

        except Exception as e:
            print("Generator error:", e)

        await asyncio.sleep(20)  # ⏱ بطيء (ممتاز)


rand = random.random()

if rand < 0.3:
    result = "SAFE"
    score = random.randint(10, 40)

elif rand < 0.7:
    result = "SUSPICIOUS"
    score = random.randint(50, 75)

else:
    result = "MALICIOUS"
    score = random.randint(80, 100)

    import asyncio
import random
from datetime import datetime
import pytz

from sqlalchemy.orm import Session
from models.base import SessionLocal
from models.alert import Alert


async def start_data_generation():
    while True:
        try:
            db: Session = SessionLocal()

            ip = f"192.168.1.{random.randint(1,255)}"
            behavior = random.choice(["normal", "ddos", "scan"])

            # 🔥 توزيع حقيقي
            rand = random.random()

            if rand < 0.4:
                result = "SAFE"
                score = random.randint(10,40)

            elif rand < 0.75:
                result = "SUSPICIOUS"
                score = random.randint(50,75)

            else:
                result = "MALICIOUS"
                score = random.randint(80,100)

            packets = random.randint(100,1500)

            db.add(Alert(
                ip=ip,
                behavior=behavior,
                packets=packets,
                result=result,
                score=score,
                created_at=datetime.now(pytz.timezone("Asia/Riyadh"))
            ))

            db.commit()
            db.close()

        except Exception as e:
            print("generator error", e)

        await asyncio.sleep(15)