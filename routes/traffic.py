from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.base import get_db
from services.auth_service import get_current_user
from services.data_service import (
    get_attack_breakdown,
    get_suspicious_ips,
    get_traffic_history
)
from services.security import rate_limit
from models.alert import Alert

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ==============================
# 🔵 Traffic Page
# ==============================
@router.get("/traffic", response_class=HTMLResponse)
def traffic_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "traffic.html",
        {"request": request, "user": user}
    )


# ==============================
# 🔵 Traffic Summary API
# ==============================
@router.get("/api/traffic/summary")
def traffic_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    _: None = Depends(rate_limit)
):
    return JSONResponse({
        "history": get_traffic_history(db),
        "attackBreakdown": get_attack_breakdown(db),
        "suspiciousIps": get_suspicious_ips(db),
    })


# ==============================
# 🔴 Network Analysis (FIXED + SAVE)
# ==============================
@router.post("/analyze-network")
async def analyze_network(
    request: Request,
    db: Session = Depends(get_db)
):
    data = await request.json()

    ip = data.get("ip", "0.0.0.0")
    behavior = data.get("behavior", "unknown")
    packets = int(data.get("packets", 0))

    # 🔴 تحليل
    if packets < 1000:
        result = "SAFE"
        score = 20
        severity = "Low"

    elif packets < 5000:
        result = "SUSPICIOUS"
        score = 60
        severity = "Medium"

    else:
        result = "MALICIOUS"
        score = 90
        severity = "High"

    # 🔴 حفظ في قاعدة البيانات (مهم)
    alert = Alert(
        title=f"Network Analysis from {ip}",
        description=f"Behavior: {behavior}",
        ip=ip,
        behavior=behavior,
        packets=packets,
        result=result,
        score=score,
        risk_score=score,
        severity_level=severity,
        resolved=False
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return {
        "result": result,
        "score": score,
        "severity": severity
    }


# ==============================
# 🔵 Alerts API (FIXED)
# ==============================
@router.get("/api/alerts/all")
def get_all_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.id.desc()).all()

    return {
        "alerts": [
            {
                "id": a.id,
                "ip": a.ip,
                "behavior": a.behavior,
                "packets": a.packets,
                "result": a.result,
                "score": a.score,
                "severity": a.severity_level,
                "createdAt": a.created_at.isoformat() if a.created_at else None
            }
            for a in alerts
        ]
    }


# ==============================
# 🔵 Network Page
# ==============================
@router.get("/network", response_class=HTMLResponse)
def network_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "network.html",
        {"request": request, "user": user}
    )


# ==============================
# 🔵 Network Data API
# ==============================
@router.get("/api/network/data")
def network_data(db: Session = Depends(get_db)):
    return {
        "history": get_traffic_history(db),
        "breakdown": get_attack_breakdown(db)
    }
@router.get("/api/alerts/live")
def live_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.id.desc()).limit(50).all()

    return {
        "alerts": [
            {
                "id": a.id,
                "ip": a.ip,
                "behavior": a.behavior,
                "packets": a.packets,
                "result": a.result,
                "score": a.score,
                "severity": a.severity_level,
                "createdAt": a.created_at.isoformat() if a.created_at else None
            }
            for a in alerts
        ]
    }
@router.get("/analysis", response_class=HTMLResponse)
def analysis_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "analysis.html",
        {"request": request, "user": user}
    )