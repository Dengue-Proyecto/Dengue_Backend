from modelo import FormularioSintomas
from utilidades import get_modelo

# Función para calcular el riesgo de dengue
def calcular_riesgo(sintomas: FormularioSintomas):
    modelo = get_modelo()
    # Convertir los síntomas del formulario en una lista de valores 0 y 1
    datos = [
        sintomas.dias_de_fiebre,
        sintomas.dolor_cabeza_severo,
        sintomas.dolor_detras_ojos,
        sintomas.dolor_articular_muscular,
        sintomas.sabor_metalico_boca,
        sintomas.perdida_apetito,
        sintomas.dolor_abdominal,
        sintomas.nauseas_vomitos,
        sintomas.diarrea
    ]
    print("Características enviadas al modelo:", datos)
    # Realizar la predicción usando el modelo
    probabilidad = modelo.predict_proba([datos])[0][1]
    print(f"Probabilidad: {probabilidad}")

    # Determinar el riesgo basado en la probabilidad
    if probabilidad < 0.3:
        return "bajo"
    elif probabilidad < 0.7:
        return "medio"
    else:
        return "alto"