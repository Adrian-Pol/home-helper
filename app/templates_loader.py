from fastapi.templating import Jinja2Templates
from app.utils.images import get_images

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["get_images"] = get_images