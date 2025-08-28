# app/routes/diary_routes.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import DiaryEntry, EntryImage, User
from app.services.diary_service import (
    update_user_diary,
    get_images_by_entries,
    custom_sort,
    read_diary_text
)
from app.templates_loader import templates
from app.schemas.diary import DiaryQuery
from app.services.auth_service import get_current_user
from app.utils.reactassets import get_react_assets
import os, shutil


router = APIRouter()


@router.get("/pamietnik")
async def show_diary_page(
    request: Request,
    query: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse("/login", status_code=303)

    # Synchronizacja wpisów użytkownika
    update_user_diary(current_user, db)
    react_js, react_css = get_react_assets()
    # Pobierz wpisy
    entries = db.query(DiaryEntry).filter(DiaryEntry.user_id == current_user.id).all()

    # Filtrowanie po query
    if query:
        entries = [
            e for e in entries
            if query.lower() in e.folder_name.lower() or query.lower() in read_diary_text(current_user.username, e.folder_name).lower()
        ]

    # Tworzymy słownik obrazków
    images_by_entry_id = get_images_by_entries(db, entries)

    # Sortowanie
    entries_sorted = sorted(entries, key=custom_sort)

    return templates.TemplateResponse("pamietnik.html", {
        "request": request,
        "entries": entries_sorted,
        "images_by_entry_id": images_by_entry_id,
        "query": query,
        "react_js": react_js,
        "react_css": react_css,
    })

@router.get("/api/pamietnik")
async def api_get_diary(
    query: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return JSONResponse({"error": "Nie zalogowany"}, status_code=401)

    update_user_diary(current_user, db)

    entries = db.query(DiaryEntry).filter(DiaryEntry.user_id == current_user.id).all()

    if query:
        entries = [
            e for e in entries
            if query.lower() in e.folder_name.lower() or query.lower() in read_diary_text(current_user.username, e.folder_name).lower()
        ]

    images_by_entry_id = get_images_by_entries(db, entries)
    entries_sorted = sorted(entries, key=custom_sort)

    result = []
    for entry in entries_sorted:
        images = images_by_entry_id.get(entry.id, [])
        # Zamiana backslash \ na slash /
        first_image = images[0].replace("\\", "/") if images else None
        result.append({
            "id": entry.id,
            "folder_name": entry.folder_name,
            "first_image": first_image
        })

    return JSONResponse(result)

@router.post("/scan-diary")
async def api_scan_diary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return JSONResponse({"error": "Nie jesteś zalogowany"}, status_code=401)

    update_user_diary(current_user, db)

    entries = db.query(DiaryEntry).filter(DiaryEntry.user_id == current_user.id).all()
    images_by_entry_id = get_images_by_entries(db, entries)
    entries_sorted = sorted(entries, key=custom_sort)

    data = []
    for entry in entries_sorted:
        images = images_by_entry_id.get(entry.id, [])
        first_image = images[0] if images else None

        data.append({
            "id": entry.id,
            "folder_name": entry.folder_name,
            "first_image": first_image
        })

    return JSONResponse(data)


@router.get("/pamietnik/wpis/{entry_id}")
async def show_entry(
    request: Request,
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse("/login", status_code=303)

    entry = db.query(DiaryEntry).filter_by(id=entry_id, user_id=current_user.id).first()
    if not entry:
        return RedirectResponse("/pamietnik", status_code=303)

    images = db.query(EntryImage).filter_by(diary_entry_id=entry.id).all()
    opis = read_diary_text(current_user.username, entry.folder_name)

    return templates.TemplateResponse("dzien.html", {
        "request": request,
        "entry": entry,
        "images": images,
        "opis": opis
    })

@router.delete("/pamietnik/api/day_delete/{entry_id}", name="day_delete")
async def day_delete(
    request: Request,
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # znajdź wpis w bazie
    entry = db.query(DiaryEntry).filter_by(id=entry_id, user_id=current_user.id).first()
    if not entry:
        return JSONResponse({"error": "Nie znaleziono dnia"}, status_code=404)

    # usuń pliki z dysku
    folder_path = os.path.join("pamietniki", current_user.username, entry.folder_name)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    # usuń wpis z bazy
    db.delete(entry)
    db.commit()

    return JSONResponse({"ok": True})