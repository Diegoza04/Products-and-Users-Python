from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import CORS_ORIGINS, SEED_ADMIN_PASSWORD, SEED_ADMIN_ROLE, SEED_ADMIN_USERNAME
from app.core.database import Base, SessionLocal, engine
from app.core.exceptions import ApiError
from app.core.security import hash_password
from app.models.message import Message
from app.models.product import Product
from app.models.user import User
from app.routers.admin import router as admin_router
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.products import router as products_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        if not db.query(User).filter(User.username == SEED_ADMIN_USERNAME).first():
            db.add(
                User(
                    username=SEED_ADMIN_USERNAME,
                    password_hash=hash_password(SEED_ADMIN_PASSWORD),
                    role=SEED_ADMIN_ROLE,
                )
            )
            db.commit()

        if not db.query(Product).first():
            db.add_all(
                [
                    Product(
                        title="Producto demo",
                        description="Ejemplo inicial para probar el frontend.",
                        price=19.99,
                        is_active=True,
                        image=None,
                    ),
                    Product(
                        title="Producto inactivo",
                        description="Visible en la base de datos pero marcado como inactivo.",
                        price=9.5,
                        is_active=False,
                        image=None,
                    ),
                ]
            )
            db.commit()

        if not db.query(Message).first():
            db.add(Message(user="System", message="Historial inicial del chat"))
            db.commit()

    yield


app = FastAPI(title="Products and Users API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ApiError)
async def handle_api_error(_request: Request, exc: ApiError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"message": "Datos invalidos", "errors": exc.errors()})


@app.exception_handler(SQLAlchemyError)
async def handle_database_error(_request: Request, _exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"message": "Error interno del servidor"})


@app.exception_handler(Exception)
async def handle_unexpected_error(_request: Request, _exc: Exception):
    return JSONResponse(status_code=500, content={"message": "Error interno del servidor"})


@app.get("/")
def healthcheck():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(products_router)
app.include_router(admin_router)
app.include_router(chat_router)