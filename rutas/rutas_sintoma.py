from datetime import datetime, UTC, timezone
from fastapi import APIRouter, Depends, HTTPException
from servicios import calcular_riesgo
from modelo import FormularioSintomas, ActualizarDiagnostico
from utilidades import obtener_usuario_actual, generar_codigo_evaluacion
from db import Evaluacion, EvaluacionSintoma, Sintoma

router = APIRouter()


@router.post("/evaluar_riesgo")
async def evaluar_riesgo(
        sintomas: FormularioSintomas,
        usuario_actual: str = Depends(obtener_usuario_actual)
):
    """
    Endpoint completo con interpretación de Gemini (para result.component)
    """
    # Calcular riesgo CON Gemini
    resultados = calcular_riesgo(sintomas, usar_gemini=True)

    # Extraer la probabilidad calculada
    probabilidad_riesgo = resultados.get("probabilidad_random_forest")

    # Convertir la probabilidad a la clasificación correspondiente
    def convertir_riesgo(prob):
        if prob < 0.4:
            return 'bajo'
        else:
            return 'alto'

    riesgo = convertir_riesgo(probabilidad_riesgo)

    # Construir diccionario de síntomas solo con los marcados como True
    sintomas_dict = sintomas.model_dump()
    # Sintomas booleanos marcados en True
    sintomas_identificados = [k for k, v in sintomas_dict.items() if isinstance(v, bool) and v]
    # Añadir días de fiebre si > 0
    if sintomas_dict.get("dias_de_fiebre", 0) > 0:
        sintomas_identificados.append(f"días de fiebre: {sintomas_dict['dias_de_fiebre']}")

    fecha_utc = datetime.now(UTC)

    # Manejar campos de tiempo opcionales
    tiempo_inicial_dt = None
    tiempo_final_dt = None
    tiempo_evaluacion_dt = None

    if sintomas.tiempo_inicial is not None:
        tiempo_inicial_dt = datetime.fromtimestamp(sintomas.tiempo_inicial / 1000, tz=timezone.utc)

    if sintomas.tiempo_final is not None:
        tiempo_final_dt = datetime.fromtimestamp(sintomas.tiempo_final / 1000, tz=timezone.utc)

    if sintomas.tiempo_evaluacion is not None:
        tiempo_evaluacion_dt = datetime.fromtimestamp(sintomas.tiempo_evaluacion / 1000, tz=timezone.utc)

    codigo_evaluacion = generar_codigo_evaluacion()

    # Guardar en BD - usar fecha_utc como fallback si tiempo_inicial_dt o tiempo_final_dt son None
    evaluacion = await Evaluacion.create(
        usuario_id=int(usuario_actual),
        codigo_evaluacion=codigo_evaluacion,
        riesgo=riesgo,
        probabilidad=probabilidad_riesgo,
        tiempo_inicial=tiempo_inicial_dt or fecha_utc,
        tiempo_final=tiempo_final_dt or fecha_utc,
        fecha=fecha_utc
    )

    for nombre_sintoma in sintomas_identificados:
        sintoma_obj, _ = await Sintoma.get_or_create(nombre=nombre_sintoma)
        await EvaluacionSintoma.create(evaluacion=evaluacion, sintoma=sintoma_obj)

    return resultados


@router.post("/evaluar_riesgo_simple")
async def evaluar_riesgo_simple(
        sintomas: FormularioSintomas,
        usuario_actual: str = Depends(obtener_usuario_actual)
):
    """
    Endpoint simplificado SIN interpretación de Gemini (para result1.component)
    Solo devuelve el riesgo de Random Forest
    """
    # Calcular riesgo SIN Gemini
    resultados = calcular_riesgo(sintomas, usar_gemini=False)

    # Extraer la probabilidad calculada
    probabilidad_riesgo = resultados.get("probabilidad_random_forest")

    # Convertir la probabilidad a la clasificación correspondiente
    def convertir_riesgo(prob):
        if prob < 0.4:
            return 'bajo'
        else:
            return 'alto'

    riesgo = convertir_riesgo(probabilidad_riesgo)

    # Construir diccionario de síntomas solo con los marcados como True
    sintomas_dict = sintomas.model_dump()

    # Sintomas booleanos marcados en True con nombres legibles
    sintomas_legibles = {
        'dolor_cabeza_severo': 'Dolor de cabeza severo',
        'dolor_detras_ojos': 'Dolor detrás de los ojos',
        'dolor_articular_muscular': 'Dolor articular/muscular',
        'sabor_metalico_boca': 'Sabor metálico en la boca',
        'perdida_apetito': 'Pérdida de apetito',
        'dolor_abdominal': 'Dolor abdominal',
        'nauseas_vomitos': 'Náuseas o vómitos',
        'diarrea': 'Diarrea'
    }

    sintomas_identificados = []
    for k, v in sintomas_dict.items():
        if isinstance(v, bool) and v and k in sintomas_legibles:
            sintomas_identificados.append(sintomas_legibles[k])

    # Añadir días de fiebre si > 0
    if sintomas_dict.get("dias_de_fiebre", 0) > 0:
        sintomas_identificados.append(f"Días de fiebre: {sintomas_dict['dias_de_fiebre']}")

    fecha_utc = datetime.now(UTC)

    # Manejar campos de tiempo opcionales
    tiempo_inicial_dt = None
    tiempo_final_dt = None
    tiempo_evaluacion_dt = None

    if sintomas.tiempo_inicial is not None:
        tiempo_inicial_dt = datetime.fromtimestamp(sintomas.tiempo_inicial / 1000, tz=timezone.utc)

    if sintomas.tiempo_final is not None:
        tiempo_final_dt = datetime.fromtimestamp(sintomas.tiempo_final / 1000, tz=timezone.utc)

    if sintomas.tiempo_evaluacion is not None:
        tiempo_evaluacion_dt = datetime.fromtimestamp(sintomas.tiempo_evaluacion / 1000, tz=timezone.utc)

    codigo_evaluacion = generar_codigo_evaluacion()

    # Guardar en BD - usar fecha_utc como fallback si tiempo_inicial_dt o tiempo_final_dt son None
    evaluacion = await Evaluacion.create(
        usuario_id=int(usuario_actual),
        codigo_evaluacion=codigo_evaluacion,
        riesgo=riesgo,
        probabilidad=probabilidad_riesgo,
        tiempo_inicial=tiempo_inicial_dt or fecha_utc,
        tiempo_final=tiempo_final_dt or fecha_utc,
        fecha=fecha_utc
    )

    for nombre_sintoma in sintomas_identificados:
        sintoma_obj, _ = await Sintoma.get_or_create(nombre=nombre_sintoma)
        await EvaluacionSintoma.create(evaluacion=evaluacion, sintoma=sintoma_obj)

    return {
        "riesgo_random_forest": resultados.get("riesgo_random_forest"),
        "probabilidad_random_forest_pct": resultados.get("probabilidad_random_forest_pct"),
        "codigo_evaluacion": codigo_evaluacion,
        "sintomas_identificados": sintomas_identificados,
        "fecha_evaluacion": fecha_utc.isoformat()
    }

@router.get("/mis_evaluaciones")
async def obtener_mis_evaluaciones(usuario_actual: str = Depends(obtener_usuario_actual)):
    evaluaciones = await Evaluacion.filter(usuario_id=int(usuario_actual)).prefetch_related("evaluacion_sintomas__sintoma").order_by("-fecha").all()
    resultados = []
    for ev in evaluaciones:
        sintomas = [es.sintoma.nombre for es in ev.evaluacion_sintomas]
        cantidad_sintomas = len(sintomas)
        tiempo_eval_segundos = (ev.tiempo_final - ev.tiempo_inicial).total_seconds()
        resultados.append({
            'id': ev.id,
            'codigo_evaluacion': ev.codigo_evaluacion,
            "fecha": ev.fecha.isoformat(),
            "riesgo": ev.riesgo,
            "resultado": ev.resultado,
            "sintomas_identificados": sintomas,
            "cantidad_sintomas": cantidad_sintomas,
            "tiempo_inicial": ev.tiempo_inicial.isoformat(),
            "tiempo_final": ev.tiempo_final.isoformat(),
            "tiempo_evaluacion": int(tiempo_eval_segundos)
        })

    return resultados

@router.get("/buscar_evaluacion/{codigo}")
async def buscar_evaluacion_por_codigo(codigo: str):
    """Buscar evaluación por código para seguimiento médico"""
    evaluacion = await Evaluacion.get_or_none(codigo_evaluacion=codigo).prefetch_related("evaluacion_sintomas__sintoma")

    if not evaluacion:
        raise HTTPException(status_code=404, detail="Código de evaluación no encontrado")

    sintomas = [es.sintoma.nombre for es in evaluacion.evaluacion_sintomas]
    cantidad_sintomas = len(sintomas)
    tiempo_eval_segundos = (evaluacion.tiempo_final - evaluacion.tiempo_inicial).total_seconds()

    return {
        'id': evaluacion.id,
        'codigo_evaluacion': evaluacion.codigo_evaluacion,
        "fecha": evaluacion.fecha.isoformat(),
        "riesgo": evaluacion.riesgo,
        "resultado": evaluacion.resultado,
        "sintomas_identificados": sintomas,
        "cantidad_sintomas": cantidad_sintomas,
        "tiempo_inicial": evaluacion.tiempo_inicial.isoformat(),
        "tiempo_final": evaluacion.tiempo_final.isoformat(),
        "tiempo_evaluacion": int(tiempo_eval_segundos)
    }

@router.put("/evaluacion/{evaluacion_id}")
async def actualizar_diagnostico_real(
    evaluacion_id: int,
    diagnostico: ActualizarDiagnostico,
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    """
    Endpoint para que un doctor actualice el riesgo real después de pruebas de laboratorio
    """
    # Buscar la evaluación
    evaluacion = await Evaluacion.get_or_none(id=evaluacion_id)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    # Validar que el resultado sea válido (ahora solo bajo o alto)
    riesgos_validos = ['bajo', 'alto', 'negativo', 'positivo']
    if diagnostico.resultado not in riesgos_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Riesgo real debe ser uno de: {', '.join(riesgos_validos)}"
        )

    # Actualizar la evaluación con el diagnóstico real
    evaluacion.resultado = diagnostico.resultado
    await evaluacion.save()

    return {
        "mensaje": "Diagnóstico real actualizado correctamente",
        "evaluacion_id": evaluacion_id,
        "resultado": diagnostico.resultado
    }