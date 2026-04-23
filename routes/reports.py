from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.base import get_db
from models.alert import Alert

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# صفحة التقارير
@router.get("/reports", response_class=HTMLResponse)
def reports_page(request: Request):
    return templates.TemplateResponse("reports.html", {
        "request": request
    })


# البيانات (مصدر واحد فقط)
@router.get("/reports/data")
def get_reports(db: Session = Depends(get_db)):

    alerts = db.query(Alert).order_by(Alert.id.desc()).limit(200).all()

    return [
        {
            "id": a.id,
            "ip": a.ip,
            "behavior": a.behavior,
            "packets": a.packets,
            "result": a.result,
            "score": a.score,
            "createdAt": a.created_at.isoformat() if a.created_at else ""
        }
        for a in alerts
    ]