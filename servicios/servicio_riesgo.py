from modelo import FormularioSintomas
from utilidades import get_modelo
import pandas as pd

def calcular_riesgo(sintomas: FormularioSintomas):
    modelo = get_modelo()  # Cargar los modelos
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

    # Convertir la lista a un DataFrame
    df_datos = pd.DataFrame([datos], columns=[
        "dias_con_fiebre",
        "dolor_cabeza_severo",
        "dolor_detras_ojos",
        "dolor_articular_muscular",
        "sabor_metalico_boca",
        "perdida_apetito",
        "dolor_abdominal",
        "nauseas_vomitos",
        "diarrea"
    ])

    # Realizar la predicción usando el modelo
    probabilidad_lineal = modelo["svm_linear"].predict_proba(df_datos)[0][1]
    probabilidad_poli = modelo["svm_poly"].predict_proba(df_datos)[0][1]
    probabilidad_rbf = modelo["svm_rbf"].predict_proba(df_datos)[0][1]
    probabilidad_sigmoid = modelo["svm_sigmoid"].predict_proba(df_datos)[0][1]
    probabilidad_random_forest = modelo["random_forest"].predict_proba(df_datos)[0][1]

    print(probabilidad_lineal)
    print(probabilidad_poli)
    print(probabilidad_rbf)
    print(probabilidad_sigmoid)
    print(probabilidad_random_forest)

    # Función para convertir la probabilidad a clasificación de riesgo
    def convertir_riesgo(prob):
        if prob < 0.3:
            return 'bajo'
        elif prob < 0.7:
            return 'medio'
        else:
            return 'alto'

    # Determinar el riesgo basado en la probabilidad para cada modelo
    riesgo_lineal = convertir_riesgo(probabilidad_lineal)
    riesgo_poli = convertir_riesgo(probabilidad_poli)
    riesgo_rbf = convertir_riesgo(probabilidad_rbf)
    riesgo_sigmoid = convertir_riesgo(probabilidad_sigmoid)
    riesgo_random_forest = convertir_riesgo(probabilidad_random_forest)

    # Convertir las probabilidades a porcentaje
    probabilidad_lineal_pct = round(probabilidad_lineal * 100, 2)
    probabilidad_poli_pct = round(probabilidad_poli * 100, 2)
    probabilidad_rbf_pct = round(probabilidad_rbf * 100, 2)
    probabilidad_sigmoid_pct = round(probabilidad_sigmoid * 100, 2)
    probabilidad_random_forest_pct = round(probabilidad_random_forest * 100, 2)

    # Devolver los riesgos
    return {
        "riesgo_lineal": riesgo_lineal,
        "riesgo_poli": riesgo_poli,
        "riesgo_rbf": riesgo_rbf,
        "riesgo_sigmoid": riesgo_sigmoid,
        "riesgo_random_forest": riesgo_random_forest,
        "probabilidad_lineal_pct": probabilidad_lineal_pct,
        "probabilidad_poli_pct": probabilidad_poli_pct,
        "probabilidad_rbf_pct": probabilidad_rbf_pct,
        "probabilidad_sigmoid_pct": probabilidad_sigmoid_pct,
        "probabilidad_random_forest_pct": probabilidad_random_forest_pct
    }