from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.base import get_db
from models.alert import Alert
from services.auth_service import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user
    })


# 🔥 SUMMARY
@router.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()

    total_traffic = sum(a.packets or 0 for a in alerts)
    threat_count = sum(1 for a in alerts if (a.result or "SAFE") != "SAFE")

    status = "OK"
    if threat_count > 20:
        status = "CRITICAL"
    elif threat_count > 5:
        status = "WARNING"

    return {
        "totalTraffic": total_traffic,
        "threatCount": threat_count,
        "status": status
    }


# 🔥 ALERTS (كان 404)
@router.get("/api/dashboard/alerts")
def dashboard_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.id.desc()).limit(20).all()

    return {
        "alerts": [
            {
                "ip": a.ip,
                "behavior": a.behavior,
                "packets": a.packets,
                "result": a.result or "SAFE",
                "score": a.score or 0,
                "createdAt": a.created_at.isoformat() if a.created_at else ""
            }
            for a in alerts
        ]
    }