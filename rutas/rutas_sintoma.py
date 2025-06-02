from datetime import datetime, UTC, timezone
from fastapi import APIRouter, Depends
from servicios import calcular_riesgo
from modelo import FormularioSintomas
from utilidades import obtener_usuario_actual
from db import Evaluacion, EvaluacionSintoma, Sintoma

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
    tiempo_inicial_dt = datetime.fromtimestamp(sintomas.tiempo_inicial / 1000, tz=timezone.utc)
    tiempo_final_dt = datetime.fromtimestamp(sintomas.tiempo_final / 1000, tz=timezone.utc)

    # Guardar en BD
    evaluacion = await Evaluacion.create(
        usuario_id=int(usuario_actual),
        riesgo=riesgo,
        tiempo_inicial=tiempo_inicial_dt,
        tiempo_final=tiempo_final_dt,
        fecha=fecha_utc
    )

    for nombre_sintoma in sintomas_identificados:
        sintoma_obj, _ = await Sintoma.get_or_create(nombre=nombre_sintoma)
        await EvaluacionSintoma.create(evaluacion=evaluacion, sintoma=sintoma_obj)

    return resultados

@router.get("/mis_evaluaciones")
async def obtener_mis_evaluaciones(usuario_actual: str = Depends(obtener_usuario_actual)):
    evaluaciones = await Evaluacion.filter(usuario_id=int(usuario_actual)).prefetch_related("evaluacion_sintomas__sintoma").order_by("-fecha").all()
    resultados = []
    for ev in evaluaciones:
        sintomas = [es.sintoma.nombre for es in ev.evaluacion_sintomas]  # lista de nombres
        cantidad_sintomas = len(sintomas)
        tiempo_eval_segundos = (ev.tiempo_final - ev.tiempo_inicial).total_seconds()
        resultados.append({
            "fecha": ev.fecha.isoformat(),
            "riesgo": ev.riesgo,
            "sintomas_identificados": sintomas,
            "cantidad_sintomas": cantidad_sintomas,
            "tiempo_inicial": ev.tiempo_inicial.isoformat(),
            "tiempo_final": ev.tiempo_final.isoformat(),
            "tiempo_evaluacion": int(tiempo_eval_segundos)
        })

    return resultados
