import os
from sqlalchemy.orm import Session
from app.models import EntryImage

def get_images(entry_id: int, db: Session):
    images = db.query(EntryImage).filter(EntryImage.diary_entry_id == entry_id).all()
    return [img.image_path for img in images]

