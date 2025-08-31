from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os
import secrets
from dotenv import load_dotenv


from app.routes import diary_routes, auth_routes, goal_routes,measurement_routes


from app.init_db import init_db
init_db()


app = FastAPI(title="Diary & Goals App")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("Brak SECRET_KEY w pliku .env!")

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


app.include_router(auth_routes.router)
app.include_router(diary_routes.router)
app.include_router(goal_routes.router)
app.include_router(measurement_routes.router)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
print(BASE_DIR)

app.mount("/pamietniki", StaticFiles(directory="pamietniki"), name="pamietniki")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/Pomiary", StaticFiles(directory="Pomiary"), name="pomiary")
app.mount(
    "/static/react",
    StaticFiles(directory=os.path.join(BASE_DIR,"static/react")),  # assets z buildu
    name="react"
)



@app.get("/", include_in_schema=False)
async def root():
    """Przekierowanie do strony logowania"""
    return RedirectResponse("/login")


@app.get("/home", include_in_schema=False)
async def home_redirect(request: Request):
    """Przekierowanie do strony użytkownika, jeśli zalogowany"""
    username = request.session.get("user")
    if username:
        return RedirectResponse(f"/home/{username}")
    return RedirectResponse("/login")


@app.get("/home/{username}")
async def user_home(request: Request, username: str):
    """Strona główna dla zalogowanego użytkownika"""
    if request.session.get("user") != username:
        return RedirectResponse("/login")
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "username": username}
    )
