from app.database import engine
from app.models import Base

def init_db():
    print("🔧 Tworzenie tabel na podstawie modeli...")
    Base.metadata.create_all(bind=engine)
    print("✅ Baza danych gotowa.")