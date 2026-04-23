from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/traffic-live", response_class=HTMLResponse)
def traffic_live(request: Request):
    return templates.TemplateResponse("traffic_live.html", {
        "request": request
    })