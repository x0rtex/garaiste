from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def garage(request: Request):
    return templates.TemplateResponse(request, "index.html", {"title": "Garage"})


@app.get("/profile")
def profile(request: Request):
    return templates.TemplateResponse(request, "profile.html", {"title": "Profile"})


@app.get("/admin")
def admin(request: Request):
    return templates.TemplateResponse(request, "admin.html", {"title": "Admin Panel"})


@app.get("/settings")
def settings(request: Request):
    return templates.TemplateResponse(request, "settings.html", {"title": "Settings"})



@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail or "An error occurred. Please check your request and try again."
    )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )
