# app/routes/symptom_routes.py

from fastapi import APIRouter
from services.risk_service import calcular_riesgo
from models.symptom_model import SymptomForm

router = APIRouter()

# Ruta para recibir los datos del formulario y devolver el riesgo de dengue
@router.post("/evaluar_riesgo")
def evaluar_riesgo(symptoms: SymptomForm):
    print(symptoms)
    # Calculamos el riesgo usando la función que definiremos más adelante en 'services/risk_service.py'
    riesgo = calcular_riesgo(symptoms)
    return {"riesgo": riesgo}
