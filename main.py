from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.api.v1.api import api_router
from app.models.user import User
from app.core.deps import Base, engine
import os

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return RedirectResponse(url="/login.html")


@app.get("/login.html")
def login_page():
    return FileResponse(os.path.join("templates", "login.html"))


@app.get("/signup.html")
def signup_page():
    return FileResponse(os.path.join("templates", "signup.html"))


@app.get("/dashboard.html")
def dashboard_page():
    return FileResponse(os.path.join("templates", "dashboard.html"))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
