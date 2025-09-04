from fastapi import FastAPI, Request, Form, status, Depends,APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse,FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_
import os
from app.database import get_db
from app.services.auth_service import get_user_by_username,login_user,register_user,verify_password,get_current_user
from app.templates_loader import templates
from app.models import GoalEntry, User
from app.services.goal_service import add_goal,remove_goal
from app.schemas.goal import GoalQuery,DeleteGoal,GoalEntrySchema
from app.utils.reactassets import get_react_assets
from typing import List


router = APIRouter()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@router.get("/cele", response_class=HTMLResponse)
async def widok_cele(current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse("/login")

    
    return FileResponse(os.path.join(BASE_DIR, "../static/react/index.html"))
@router.get("/api/cele",response_model=List[GoalEntrySchema])
async def api_get_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return JSONResponse({"error": "Nie jesteś zalogowany"}, status_code=401)

    
    goals = db.query(GoalEntry).filter(GoalEntry.user_id == current_user.id).order_by(GoalEntry.priority.asc()).all()
    
    
    

    return goals

@router.post("/cele")
async def dodaj_cel(
    request: Request,
    goaldata: GoalQuery = Depends(GoalQuery.from_request),
    db: Session = Depends(get_db),
    currenet_user: User = Depends(get_current_user) 
    ):
    try:
        add_goal(goaldata.cele, goaldata.ocena, currenet_user.username, db)
        return JSONResponse(content={"message": "Cel dodany"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error":str(e)}, status_code=500)





@router.delete("/cele/{entry_id}")
async def goal_delete(
    request: Request,
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        remove_goal(entry_id,current_user.username,db)
        return JSONResponse(content={"message": "Cel usunięty"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
