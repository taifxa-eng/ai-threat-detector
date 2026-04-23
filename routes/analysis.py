from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from services.auth_service import get_current_user
from models.base import get_db
from models.alert import Alert

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ================= صفحات =================

@router.get("/alerts", response_class=HTMLResponse)
def alerts_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("alerts.html", {"request": request})


@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("settings.html", {"request": request})


@router.get("/traffic-live", response_class=HTMLResponse)
def live_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("traffic_live.html", {"request": request})


# ================= SETTINGS (مو مكرر الآن) =================

@router.post("/api/settings")
def update_settings(data: dict):
    return {"status": "saved", "data": data}

@router.get("/dev/clear-alerts")
def clear_alerts(db: Session = Depends(get_db)):
    db.query(Alert).delete()
    db.commit()
    return {"status": "cleared"}

# ================= 🔥 ANALYZE + AUTO SAVE =================

@router.post("/analyze-network")
def analyze(data: dict, db: Session = Depends(get_db)):

    ip = data.get("ip")
    behavior = data.get("behavior")
    packets = int(data.get("packets", 0))

    # 🔥 منطق ذكي مو ثابت
    if packets > 1000:
        result = "MALICIOUS"
        score = 90

    elif packets > 600:
        result = "SUSPICIOUS"
        score = 65

    else:
        result = "SAFE"
        score = 30

    # 🔥 مهم جدًا: حفظ فعلي
    new_alert = Alert(
        ip=ip,
        behavior=behavior,
        packets=packets,
        result=result,
        score=score
    )

    db.add(new_alert)
    db.commit()

    return {
        "result": result,
        "score": score
    }

    # 🔥 تحليل بسيط (نفس نظامك بدون تخريب)
    score = 0
    result = "SAFE"


    if packets > 1000:
        score += 50
    if behavior and behavior.lower() in ["ddos", "malware"]:
        score += 40

    if score >= 80:
        result = "MALICIOUS"
    elif score >= 50:
        result = "SUSPICIOUS"
       

    # ===============================
    # 🔥 حفظ تلقائي في التقارير
    # ===============================
    try:
        alert = Alert(
            ip=ip,
            behavior=behavior,
            packets=packets,
            result=result,
            score=score
        )
        db.add(alert)
        db.commit()
    except Exception as e:
        print("Save error:", e)

    return {
        "ip": ip,
        "behavior": behavior,
        "packets": packets,
        "result": result,
        "score": score
    }
# بدل return الحالي خلي:
    return {
    "ip": ip,
    "behavior": behavior,
    "packets": packets,
    "result": result,
    "score": score,
    "status": result  # 🔥 مهم عشان الفرونت
}