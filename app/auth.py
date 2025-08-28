import bcrypt
from sqlalchemy.orm import Session
from app.models import User

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False

def login_user(db: Session, username: str, password: str) -> bool:
    user = get_user_by_username(db, username)
    if not user:
        return False
    return verify_password(password, user.password)

def register_user(username: str, password: str, db: Session):
    if get_user_by_username(db, username):
        
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
