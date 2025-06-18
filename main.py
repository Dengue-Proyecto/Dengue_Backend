from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rutas import sintoma_router, usuario_router
from tortoise.contrib.fastapi import register_tortoise
from config import settings

app = FastAPI()

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["db.usuario", "db.evaluacion", "db.sintoma", "db.evaluacion_sintoma"]},  # Asegúrate de incluir todos los modelos necesarios
    generate_schemas=True,  # True para crear las tablas automáticamente
    add_exception_handlers=True,
)

# Configuración de CORS
origins = [
    "http://localhost:4200",  # Frontend en Angular (puerto por defecto)
    "https://riesgodengue.netlify.app",  # URL de tu frontend si está desplegado en producción
]

# Configuración de CORS - Forma estándar
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],
)

app.include_router(sintoma_router)
app.include_router(usuario_router)