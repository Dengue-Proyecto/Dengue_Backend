from fastapi import APIRouter
from servicios import calcular_riesgo
from modelo import FormularioSintomas
router = APIRouter()
# Ruta para recibir los datos del formulario y devolver el riesgo de dengue

@router.post("/evaluar_riesgo")
def evaluar_riesgo(sintomas: FormularioSintomas):
    print(sintomas)
    # Calculamos el riesgo usando la función que definiremos más adelante en 'servicios/servicio_riesgo.py'
    riesgo = calcular_riesgo(sintomas)
    return {"riesgo": riesgo}
