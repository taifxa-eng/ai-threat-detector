from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from models.base import get_db
from services.auth_service import get_current_user, hash_password, verify_password
from services.security import rate_limit
from models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("settings.html", {"request": request, "user": user})


@router.post("/api/settings/password")
def update_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    _: None = Depends(rate_limit),
):
    target = db.query(User).filter(User.id == user.id).first()
    if not target:
        return JSONResponse({"success": False, "message": "User not found."}, status_code=status.HTTP_404_NOT_FOUND)
    if not verify_password(current_password, target.hashed_password):
        return JSONResponse({"success": False, "message": "Current password is incorrect."}, status_code=status.HTTP_401_UNAUTHORIZED)
    if current_password == new_password:
        return JSONResponse({"success": False, "message": "New password must be different."}, status_code=status.HTTP_400_BAD_REQUEST)
    target.hashed_password = hash_password(new_password)
    db.commit()
    return JSONResponse({"success": True, "message": "Password updated successfully."})
