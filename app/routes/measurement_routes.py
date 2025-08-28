from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.measurement_service import (
    sync_measurements_full,
    get_images_by_entries,
    add_measurement
)
from app.services.auth_service import get_current_user
from app.models import User, MeasurementEntry
from app.templates_loader import templates
from app.schemas.measurment import MeasurmentQuery
import json
import os
from datetime import date
from app.utils.reactassets import get_react_assets

router = APIRouter()




# ------------------------
# Widok /pomiary – kafelki React
# ------------------------
@router.get("/pomiary")
def widok_pomiarow(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return JSONResponse({"error":"Nie jesteś zalogowany"},status_code=401)
    # Synchronizujemy wszystkie wpisy użytkownika
    sync_measurements_full(current_user.username, db)

    # Pobieramy wszystkie wpisy
    entries = db.query(MeasurementEntry).filter(
        MeasurementEntry.user_id == current_user.id
    ).all()

    images_by_entry_id = get_images_by_entries(db, entries)

    # Pliki React (manifest.json)
    react_js, react_css = get_react_assets()

    return templates.TemplateResponse(
        "pomiar.html",
        {
            "request": request,
            "entries": entries,
            "images_by_entry_id": images_by_entry_id,
            "react_js": react_js,
            "react_css": react_css,
        }
    )


# ------------------------
# Endpoint POST – dodaj pomiar
# ------------------------
@router.post("/pomiary")
def dodaj_pomiar_route(
    measurmentdata: MeasurmentQuery = Depends(MeasurmentQuery.from_request),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        add_measurement(measurmentdata, current_user.username, db)
        return JSONResponse(content={"message": "Dodano pomiar"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------
# Widok /pomiary/lista 
# ------------------------
@router.get("/pomiary/lista", name="pomiary_lista")
def widok_listy_pomiarow(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Pobieramy wszystkie unikalne dni pomiarowe użytkownika
    dni = db.query(MeasurementEntry.entry_date).filter(
        MeasurementEntry.user_id == current_user.id
    ).distinct().all()

    
    dni = [d[0] for d in dni]
    react_js, react_css = get_react_assets()
    return templates.TemplateResponse(
        "pomiary_lista.html",
        {
            "request": request,
            "dni": dni,
            "react_js": react_js,
            "react_css": react_css,
        }
    )


@router.get("/pomiary/zarzadzaj", name="pomiary_manage")
def pomiary_manage(
    request: Request,
    
):
  
    return templates.TemplateResponse("pomiary_manage.html",{"request":request})


@router.get("/pomiary/dni")
def get_days_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entries = db.query(MeasurementEntry.id, MeasurementEntry.entry_date)\
                .filter(MeasurementEntry.user_id == current_user.id)\
                .order_by(MeasurementEntry.entry_date.desc())\
                .all()
    sync_measurements_full(current_user.username,db)
    # Zamiana na listę słowników z id i datą
    data = [
        {"id": entry.id, "day": entry.entry_date.strftime("%d-%m-%Y")}
        for entry in entries
    ]
    return JSONResponse(content=data)    

@router.get("/pomiary/dni/{measure_day}")
async def show_measure_day(
    request: Request,
    measure_day: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse("/login", status_code=303)

    entry = db.query(MeasurementEntry).filter_by(id=measure_day, user_id=current_user.id).first()
    if not entry:
        return RedirectResponse("/pomiary/lista", status_code=303)