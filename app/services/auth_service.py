import bcrypt
from sqlalchemy.orm import Session
from app.models import User
from fastapi import Request,Depends,HTTPException
from fastapi.responses import RedirectResponse
from app.database import get_db
from typing import Optional

def get_user_by_username(db: Session, username: str) ->Optional[User]:
    return db.query(User).filter(User.username == username).first()

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    try:
        if isinstance(hashed_password,str):
            hashed_bytes = hashed_password.encode("utf-8")
        else:
            hashed_bytes = hashed_password
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_bytes)
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False
def authenticate_user(db: Session, username: str, password: str)->Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
def login_user(db: Session, username: str, password: str) -> bool:
    user = get_user_by_username(db, username)
    if not user:
        return False
    return verify_password(password, user.password)

def register_user(username: str, password: str, db: Session):
    if get_user_by_username(db, username):
        # Użytkownik już istnieje
        return None
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # bytes
    user = User(username=username, password=hashed_pw)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        print("Błąd podczas rejestracji", e)
        return None

def get_current_user(
        request: Request, db: Session = Depends(get_db)
) -> User:
    username = request.session.get("user")
    if not username:
        raise HTTPException(status_code=401,detail="Nie jesteś zalogowany")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Użytkownik nie istnieje")
    
    return user