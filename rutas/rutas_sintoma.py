from fastapi import APIRouter
from servicios import calcular_riesgo
from modelo import FormularioSintomas
router = APIRouter()

@router.post("/evaluar_riesgo")
def evaluar_riesgo(sintomas: FormularioSintomas):
        print(sintomas)
        resultados = calcular_riesgo(sintomas)
        return resultados
