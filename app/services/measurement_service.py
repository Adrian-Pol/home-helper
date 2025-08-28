from sqlalchemy.orm import Session
from app.models import User, MeasurementEntry, MeasurementImage
from pathlib import Path
import sys
from datetime import date,datetime
from app.utils import dates

# 🔹 Ustalanie ścieżki bazowej aplikacji
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).resolve().parents[2]
else:
    BASE_DIR = Path(__file__).resolve().parents[2]


def add_measurement(measurmentdata, username: str, db: Session):
    """Dodaje nowy pomiar dla użytkownika."""
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise Exception("Nie znaleziono użytkownika")

    new_measurement = MeasurementEntry(
        waga=measurmentdata.waga,
        pas=measurmentdata.pas,
        posladek=measurmentdata.posladek,
        klatka=measurmentdata.klatka,
        udo_l=measurmentdata.udo_l,
        udo_p=measurmentdata.udo_p,
        lydka_l=measurmentdata.lydka_l,
        lydka_p=measurmentdata.lydka_p,
        biceps_l = measurmentdata.biceps_l,
        biceps_p = measurmentdata.biceps_p,
        entry_date=measurmentdata.entry_date or date.today(),
        folder_name=measurmentdata.folder_name,
        user_id=user.id
        )

    try:
        db.add(new_measurement)
        db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(f"Nie udało się dodać pomiaru: {e}")



def sync_measurements_full(username: str, db: Session):
    """Synchronizacja folderów Pomiary <-> baza danych"""
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise Exception("Nie znaleziono użytkownika")

    user_folder = BASE_DIR / "Pomiary" / username
    user_folder.mkdir(parents=True, exist_ok=True)

    # ------------------
    # Dysk -> baza
    # ------------------
    for date_folder in user_folder.iterdir():
        if not date_folder.is_dir():
            continue
        folder_name = date_folder.name
        opis_file = date_folder / "opis.txt"
        if not opis_file.exists():
            continue

        # Parsujemy opis.txt
        data_dict = {}
        with open(opis_file, "r", encoding="utf-8") as f:
            for line in f.read().splitlines():
                if "=" in line:
                    key, value = line.split("=")
                    data_dict[key.strip()] = float(value.strip())

        # Szukamy wpisu w bazie
        entry = db.query(MeasurementEntry).filter_by(
            user_id=user.id,
            folder_name=folder_name
        ).first()

        if entry:
            # Aktualizacja pól jeśli różnią się od pliku
            updated = False
            try:
                expected_date = dates.parse_date_from_folder(folder_name)
                if entry.entry_date != expected_date:
                    entry.entry_date = expected_date
                    updated = True
            except ValueError:
                print(f"❌ Folder ma zły format daty: {folder_name}")
            for field in ["waga","pas","posladek","klatka","udo_l","udo_p","lydka_l","lydka_p","biceps_l","biceps_p"]:
                val = int(data_dict.get(field, 0)) if field != "waga" else data_dict.get(field, 0)
                if getattr(entry, field) != val:
                    setattr(entry, field, val)
                    updated = True
            if updated:
                db.commit()
        
        else:

            try:
                entry_date = dates.parse_date_from_folder(folder_name)
            except ValueError:
                # Jeśli folder ma zły format, np. "random", pomijamy go
                print(f"❌ Niepoprawny format folderu: {folder_name}")
                continue
            # Nowy wpis
            entry = MeasurementEntry(
                user_id=user.id,
                folder_name=folder_name,
                entry_date = entry_date,
                waga=data_dict.get("waga", 0),
                pas=int(data_dict.get("pas", 0)),
                posladek=int(data_dict.get("posladek", 0)),
                klatka=int(data_dict.get("klatka", 0)),
                udo_l=int(data_dict.get("udo_l", 0)),
                udo_p=int(data_dict.get("udo_p", 0)),
                lydka_l=int(data_dict.get("lydka_l", 0)),
                lydka_p=int(data_dict.get("lydka_p", 0)),
                biceps_l=int(data_dict.get("biceps_l", 0)),
                biceps_p=int(data_dict.get("biceps_p",0))
            )
            db.add(entry)
            db.commit()

        # Synchronizacja zdjęć dysk -> baza
        existing_images = {Path(img.image_path).name for img in entry.measure_image}
        for img_file in date_folder.iterdir():
            if img_file.suffix.lower() in [".jpg", ".png"]:
                if img_file.name not in existing_images:
                    new_image = MeasurementImage(
                        measurement_entry_id=entry.id,
                        image_path=str(img_file)
                    )
                    db.add(new_image)
        db.commit()

    # ------------------
    # Baza -> dysk
    # ------------------
    entries = db.query(MeasurementEntry).filter_by(user_id=user.id).all()
    for entry in entries:
        folder_path = user_folder / entry.folder_name
        
        folder_path.mkdir(parents=True, exist_ok=True)

        # Synchronizacja opis.txt
        opis_file = folder_path / "opis.txt"
        write_file = False
        if not opis_file.exists():
            write_file = True
        else:
            disk_data = {}
            with open(opis_file, "r", encoding="utf-8") as f:
                for line in f.read().splitlines():
                    if "=" in line:
                        key, value = line.split("=")
                        disk_data[key.strip()] = float(value.strip())
            for field in ["waga","pas","posladek","klatka","udo_l","udo_p","lydka_l","lydka_p","biceps_l","biceps_p"]:
                if disk_data.get(field) != getattr(entry, field):
                    write_file = True
                    break

        if write_file:
            with open(opis_file, "w", encoding="utf-8") as f:
                f.write(f"waga={entry.waga}\n")
                f.write(f"pas={entry.pas}\n")
                f.write(f"posladek={entry.posladek}\n")
                f.write(f"klatka={entry.klatka}\n")
                f.write(f"udo_l={entry.udo_l}\n")
                f.write(f"udo_p={entry.udo_p}\n")
                f.write(f"lydka_l={entry.lydka_l}\n")
                f.write(f"lydka_p={entry.lydka_p}\n")
                f.write(f"biceps_l={entry.biceps_l}\n")
                f.write(f"biceps_p={entry.biceps_p}\n")

      

def get_images_by_entries(db: Session, entries: list[MeasurementEntry]) -> dict[int, list[str]]:
    """Zwraca dict: entry.id -> lista URLi zdjęć dla szablonu"""
    images_dict = {}
    for entry in entries:
        
        images = db.query(MeasurementImage).filter_by(measurement_entry_id=entry.id).all()
        urls = []  
        for img in images:
            try:
                relative_path = Path(img.image_path).relative_to(BASE_DIR / "Pomiary")
                urls.append(f"Pomiary/{relative_path.as_posix()}")
            except ValueError:
                continue
        
        images_dict[entry.id] = urls
    return images_dict
