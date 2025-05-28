from datetime import datetime,UTC
from fastapi import APIRouter, Depends
from servicios import calcular_riesgo
from modelo import FormularioSintomas
from utilidades import obtener_usuario_actual
from db import Evaluacion
router = APIRouter()

@router.post("/evaluar_riesgo")
async def evaluar_riesgo(
    sintomas: FormularioSintomas,
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    # Calcular riesgo
    resultados = calcular_riesgo(sintomas)

    # Extraer el riesgo de uno de los modelos (por ejemplo riesgo_lineal)
    riesgo = resultados.get("riesgo_random_forest", "desconocido")

    # Construir diccionario de síntomas solo con los marcados como True
    sintomas_dict = sintomas.dict()
    # Sintomas booleanos marcados en True
    sintomas_identificados = [k for k, v in sintomas_dict.items() if isinstance(v, bool) and v]
    # Añadir días de fiebre si > 0
    if sintomas_dict.get("dias_de_fiebre", 0) > 0:
        sintomas_identificados.append(f"días de fiebre: {sintomas_dict['dias_de_fiebre']}")

    fecha_utc = datetime.now(UTC)

    # Guardar en BD
    await Evaluacion.create(
        usuario_id=int(usuario_actual),
        riesgo=riesgo,
        sintomas=sintomas_identificados,
        tiempo_evaluacion=sintomas.tiempo_evaluacion,
        fecha=fecha_utc
    )

    return resultados

@router.get("/mis_evaluaciones")
async def obtener_mis_evaluaciones(usuario_actual: str = Depends(obtener_usuario_actual)):
    evaluaciones = await Evaluacion.filter(usuario_id=int(usuario_actual)).order_by("-fecha").all()
    resultados = []
    for ev in evaluaciones:
        sintomas = ev.sintomas or []
        cantidad_sintomas = len(sintomas)
        resultados.append({
            "fecha": ev.fecha.isoformat(),
            "riesgo": ev.riesgo,
            "sintomas_identificados": sintomas,
            "cantidad_sintomas": cantidad_sintomas,
            "tiempo_evaluacion": ev.tiempo_evaluacion
        })
    return resultados
