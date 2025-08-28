from sqlalchemy.orm import Session
from app.models import User, GoalEntry
from fastapi import HTTPException

def add_goal(goal_text: str, priority: int, username: str, db: Session) -> GoalEntry:
    """Dodaje nowy cel dla użytkownika"""
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Nie znaleziono użytkownika")

    new_goal = GoalEntry(goal=goal_text, priority=priority, user_id=user.id)
    try:
        db.add(new_goal)
        db.commit()
        db.refresh(new_goal)
        return new_goal
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd dodania celu: {e}")


def remove_goal(goal_id: int, username: str, db: Session):
    """Usuwa cel użytkownika po ID"""
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Nie znaleziono użytkownika")

    goal_to_delete = db.query(GoalEntry).filter_by(id=goal_id, user_id=user.id).first()
    if not goal_to_delete:
        raise HTTPException(status_code=404, detail="Nie znaleziono celu")

    try:
        db.delete(goal_to_delete)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd usunięcia celu: {e}")
