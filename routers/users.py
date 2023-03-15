import sys
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import APIRouter, Depends, Request, Form
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user, get_password_hash, verify_password


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"description": "Not Authorized"}}
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/changepassword", response_class=HTMLResponse)
async def change_password_page(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("passwordchange.html", {"request": request})

@router.post("/changepassword", response_class=HTMLResponse)
async def change_password(request: Request, username: str = Form(...),
                          password: str = Form(...), newpassword: str = Form(...),
                          db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    if user_model.username == username and verify_password(password, user_model.hashed_password):
        hash_newpassword = get_password_hash(newpassword)
        user_model.hashed_password = hash_newpassword
        db.add(user_model)
        db.commit()
    else:
        msg = "Username or Password Incorrect"
        return templates.TemplateResponse("passwordchange.html", {"request": request, "msg": msg})

    msg = "Password Changed Successfully"
    return templates.TemplateResponse("passwordchange.html", {"request": request, "msg": msg, "user": user})