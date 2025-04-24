from fastapi import APIRouter
from services import calcular_riesgo
from models import FormularioSintomas

router = APIRouter()

# Ruta para recibir los datos del formulario y devolver el riesgo de dengue
@router.post("/evaluar_riesgo")
def evaluar_riesgo(sintomas: FormularioSintomas):
    print(sintomas)
    # Calculamos el riesgo usando la función que definiremos más adelante en 'services/risk_service.py'
    riesgo = calcular_riesgo(sintomas)
    return {"riesgo": riesgo}
