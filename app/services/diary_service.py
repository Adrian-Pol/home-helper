import os
from datetime import datetime
from pathlib import Path
import sys
from sqlalchemy.orm import Session

from app.models import EntryImage, DiaryEntry,User
from app.auth import get_user_by_username



if getattr(sys, 'frozen', False):
   
    BASE_DIR = Path(sys.executable).resolve().parents[2]
else:
    
    BASE_DIR = Path(__file__).resolve().parents[2]


def update_user_diary(user: User, db: Session):
    """
    Aktualizuje wpisy pamiętnika użytkownika na podstawie folderów i plików w systemie.
    - Dodaje nowe wpisy jeśli pojawiły się nowe foldery
    - Usuwa wpisy jeśli folder został usunięty
    - Aktualizuje opisy jeśli zmienił się plik opis.txt
    """
   

    user_folder = BASE_DIR / "pamietniki" / user.username
   

    if not user_folder.exists():
       
        return

    # Lista folderów fizycznych na dysku
    physical_folders = {f.name for f in user_folder.iterdir() if f.is_dir()}
    

    # Lista wpisów w bazie
    db_entries = db.query(DiaryEntry).filter(DiaryEntry.user_id == user.id).all()
    db_folders = {entry.folder_name: entry for entry in db_entries}
   

    try:
        #  Usuwanie wpisów, których foldery zostały skasowane
        for folder_name, entry in list(db_folders.items()):
            if folder_name not in physical_folders:
                print(f"🗑️ Usuwam wpis: {folder_name}")
                db.delete(entry)

        #  Dodawanie lub aktualizowanie wpisów
        for folder_name in physical_folders:
            full_path = user_folder / folder_name
            opis_path = full_path / "opis.txt"

            opis = opis_path.read_text(encoding="utf-8") if opis_path.exists() else ""

            try:
                entry_date = datetime.strptime(folder_name, "%d.%m.%Y").date()
            except ValueError:
                entry_date = None

            if folder_name in db_folders:
                # Aktualizacja opisu
                entry = db_folders[folder_name]
                if entry.description != opis:
                    print(f"🔄 Aktualizuję opis wpisu {folder_name}")
                    entry.description = opis
            else:
                # Nowy wpis
                new_entry = DiaryEntry(
                    user_id=user.id,
                    entry_date=entry_date,
                    folder_name=folder_name,
                    description=opis
                )
                db.add(new_entry)
                db.flush()
                print(f"📝 Dodano nowy wpis: {folder_name}")

                # Dodanie zdjęć
                for file_name in os.listdir(full_path):
                    if file_name.lower().endswith(".jpg"):
                        img_path = os.path.join("pamietniki", user.username, folder_name, file_name)
                        db.add(EntryImage(
                            diary_entry_id=new_entry.id,
                            image_path=img_path
                        ))

        db.commit()
        print("✅ Zmiany zapisane do bazy.")
    except Exception as e:
        db.rollback()
        print("❌ Błąd podczas aktualizacji pamiętnika:", e)
def get_images_by_entries(db: Session, entries: list[DiaryEntry]) -> dict[int, list[str]]:
    """Zwraca dict: entry.id -> lista ścieżek obrazów"""
    return {
        entry.id: [
            img.image_path
            for img in db.query(EntryImage).filter_by(diary_entry_id=entry.id).all()
        ]
        for entry in entries
    }


def custom_sort(entry: DiaryEntry):
    """Sortowanie wpisów: najpierw wg daty, potem alfabetycznie po folder_name"""
    if entry.entry_date is None:
        return (0, entry.folder_name.lower())
    return (1, entry.entry_date)


def read_diary_text(username: str, folder_name: str) -> str:
    """Wczytuje opis wpisu z pliku opis.txt"""
    opis_txt_path = BASE_DIR / "pamietniki" / username / folder_name / "opis.txt"
    if opis_txt_path.is_file():
        return opis_txt_path.read_text(encoding="utf-8")
    return ""
