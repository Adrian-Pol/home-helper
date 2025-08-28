from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
import secrets
import os

from app.database import get_db
from app.services.auth_service import (
    authenticate_user,
    register_user,
)
from app.templates_loader import templates

router = APIRouter( tags=["auth"])


# -----------------------------
# LOGIN
# -----------------------------
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    """Wyświetla formularz logowania z tokenem CSRF"""
    csrf_token = request.session.get("csrf_token") or secrets.token_urlsafe(32)
    request.session['csrf_token'] = csrf_token
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None, "csrf_token": csrf_token}
    )


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    """Logowanie użytkownika - obsługa JSON i formularza"""
    content_type = request.headers.get('content-type', '').lower()
    is_json = 'application/json' in content_type

    # Pobranie danych
    if is_json:
        payload = await request.json()
        username = payload.get('username')
        password = payload.get('password')
        csrf = request.headers.get('X-CSRF-Token')
    else:
        form = await request.form()
        username = form.get('username')
        password = form.get('password')
        csrf = form.get('csrf_token')

    # Walidacja pól
    if not username or not password:
        error_msg = "Uzupełnij wszystkie pola"
        if is_json:
            return JSONResponse({'ok': False, 'error': error_msg}, status_code=400)
        return templates.TemplateResponse("login.html", {"request": request, "error": error_msg, "csrf_token": request.session.get('csrf_token')})

    # Walidacja CSRF
    if csrf != request.session.get('csrf_token'):
        error_msg = "Błąd CSRF"
        if is_json:
            return JSONResponse({'ok': False, 'error': error_msg}, status_code=403)
        return templates.TemplateResponse("login.html", {"request": request, "error": error_msg, "csrf_token": request.session.get('csrf_token')})

    # Autoryzacja użytkownika
    user = authenticate_user(db, username, password)
    if not user:
        error_msg = "Nieprawidłowe dane"
        if is_json:
            return JSONResponse({'ok': False, 'error': error_msg}, status_code=401)
        return templates.TemplateResponse("login.html", {"request": request, "error": error_msg, "csrf_token": request.session.get('csrf_token')})

    # Zapis sesji i odświeżenie CSRF
    request.session['user'] = user.username
    request.session['csrf_token'] = secrets.token_urlsafe(32)

    # Odpowiedź
    if is_json:
        return JSONResponse({'ok': True, 'redirect': f'/home/{user.username}'})
    return RedirectResponse(f'/home/{user.username}', status_code=status.HTTP_303_SEE_OTHER)


# -----------------------------
# REGISTER
# -----------------------------
@router.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    """Wyświetla formularz rejestracji z tokenem CSRF"""
    csrf_token = request.session.get('csrf_token') or secrets.token_urlsafe(32)
    request.session['csrf_token'] = csrf_token
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "error": None, "csrf_token": csrf_token}
    )


@router.post("/register")
async def process_registration(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Rejestracja użytkownika"""
    form = await request.form()
    csrf = form.get("csrf_token")
    if csrf != request.session.get("csrf_token"):
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Błąd CSRF", "csrf_token": request.session.get("csrf_token")}
        )

    user = register_user(username, password, db)
    if not user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Rejestracja nie powiodła się lub użytkownik już istnieje",
             "csrf_token": request.session.get("csrf_token")}
        )

    # Tworzenie katalogu użytkownika
    os.makedirs(os.path.join("pamietniki", username), exist_ok=True)
    os.makedirs(os.path.join("Pomiary", username), exist_ok=True)
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


# -----------------------------
# LOGOUT
# -----------------------------
@router.get("/logout", response_class=HTMLResponse)
@router.post("/logout")
async def logout(request: Request):
    """Wylogowanie użytkownika i czyszczenie sesji"""
    request.session.clear()
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
