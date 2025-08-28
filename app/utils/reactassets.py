from pathlib import Path
from fastapi.responses import JSONResponse
import os
import json

def get_react_assets():
    """Odczytaj pliki JS i CSS React z manifest.json"""
    manifest_path = os.path.join("app", "static", "react",".vite", "manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    entry = manifest["src/main.jsx"]
    return entry["file"], entry.get("css", [])