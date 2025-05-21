from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rutas import sintoma_router

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:4200",  # Frontend en Angular (puerto por defecto)
    "https://riesgodengue.netlify.app",  # URL de tu frontend si está desplegado en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir los dominios del frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los encabezados
)
app.include_router(sintoma_router)

