from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.config import WEB_ADMIN_PASSWORD, WEB_ADMIN_USERNAME
from app.database.connection import initialize_database
from app.database.repositories import get_stats

app = FastAPI(title="MODYX GAMING Admin")
app.add_middleware(SessionMiddleware, secret_key="modyx-gaming-secret-key")
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")
templates = Jinja2Templates(directory="app/web/templates")


def is_admin_logged_in(request: Request) -> bool:
    return bool(request.session.get("admin_logged_in"))


@app.get("/", response_class=RedirectResponse)
async def root_redirect():
    return RedirectResponse("/login")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if is_admin_logged_in(request):
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login_submit(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    if not WEB_ADMIN_USERNAME or not WEB_ADMIN_PASSWORD:
        return templates.TemplateResponse("login.html", {"request": request, "error": "قم بإعداد بيانات لوحة الإدارة في app/config.py."})

    if username == WEB_ADMIN_USERNAME and password == WEB_ADMIN_PASSWORD:
        request.session["admin_logged_in"] = True
        return RedirectResponse("/dashboard", status_code=302)

    return templates.TemplateResponse("login.html", {"request": request, "error": "اسم المستخدم أو كلمة المرور غير صحيحة."})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not is_admin_logged_in(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "stats": get_stats()})


@app.get("/api/health")
async def api_health():
    return {"status": "ok", "service": "MODYX GAMING", "database": "sqlite"}


@app.get("/api/tournaments")
async def api_tournaments():
    from app.database.connection import get_connection
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM tournaments ORDER BY id DESC LIMIT 20").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


@app.get("/api/registrations")
async def api_registrations():
    from app.database.connection import get_connection
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM registrations ORDER BY id DESC LIMIT 20").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")


initialize_database()
