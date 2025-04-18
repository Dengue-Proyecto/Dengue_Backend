from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.sypmtom_routes import router as symptom_router

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:4200",  # Frontend en Angular (puerto por defecto)
    "https://your-frontend-url.com",  # URL de tu frontend si está desplegado en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir los dominios del frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/")
async def root():
    return {"message": "Hola, Bienvenido a la API que valorará tu riesgo de dengue"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
app.include_router(symptom_router)

