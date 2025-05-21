from modelo import FormularioSintomas
from utilidades import get_modelo
from utilidades import get_metricas
from utilidades import get_preprocesadores
import pandas as pd

def calcular_riesgo(sintomas: FormularioSintomas):
    modelo = get_modelo()  # Cargar los modelos
    metricas = get_metricas() # Cargar las métricas
    scaler, pca = get_preprocesadores()  # Cargar los preprocesadores
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

    # Separar numéricas y no numéricas igual que en entrenamiento
    columnas_numericas = ['dias_con_fiebre']
    columnas_no_numericas = ['dolor_cabeza_severo', 'dolor_detras_ojos', 'dolor_articular_muscular',
                             'sabor_metalico_boca', 'perdida_apetito', 'dolor_abdominal',
                             'nauseas_vomitos', 'diarrea']

    # 1. Escalar solo las columnas numéricas (usar el scaler cargado)
    df_datos[columnas_numericas] = scaler.transform(df_datos[columnas_numericas])

    # 2. Aplicar PCA a todas las columnas (numéricas + no numéricas)
    columnas_completas = columnas_numericas + columnas_no_numericas
    datos_pca = pca.transform(df_datos[columnas_completas])

    # Convertir a DataFrame para pasar al modelo
    df_pca = pd.DataFrame(datos_pca, columns=[f'Componente {i+1}' for i in range(datos_pca.shape[1])])

    # Realizar la predicción usando el modelo
    probabilidad_lineal = modelo["svm_linear"].predict_proba(df_pca)[0][1]
    probabilidad_poli = modelo["svm_poly"].predict_proba(df_pca)[0][1]
    probabilidad_rbf = modelo["svm_rbf"].predict_proba(df_pca)[0][1]
    probabilidad_sigmoid = modelo["svm_sigmoid"].predict_proba(df_pca)[0][1]
    probabilidad_random_forest = modelo["random_forest"].predict_proba(df_datos)[0][1]
    probabilidad_xgboost = float(modelo["xgboost"].predict_proba(df_datos)[0][1])


    print(probabilidad_lineal)
    print(probabilidad_poli)
    print(probabilidad_rbf)
    print(probabilidad_sigmoid)
    print(probabilidad_random_forest)
    print(probabilidad_xgboost)

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
    riesgo_xgboost = convertir_riesgo(probabilidad_xgboost)

    # Convertir las probabilidades a porcentaje
    probabilidad_lineal_pct = round(probabilidad_lineal * 100, 2)
    probabilidad_poli_pct = round(probabilidad_poli * 100, 2)
    probabilidad_rbf_pct = round(probabilidad_rbf * 100, 2)
    probabilidad_sigmoid_pct = round(probabilidad_sigmoid * 100, 2)
    probabilidad_random_forest_pct = round(probabilidad_random_forest * 100, 2)
    probabilidad_xgboost_pct = round(probabilidad_xgboost * 100, 2)

    # Convertir las métricas en porcentaje excepto prediction_time
    metricas_pct = {}
    for modelo, met in metricas.items():
        metricas_pct[modelo] = {
            "accuracy": round(met["accuracy"] * 100, 2),
            "auc_roc": round(met["auc_roc"] * 100, 2),
            "recall": round(met["recall"] * 100, 2),
            "specificity": round(met["specificity"] * 100, 2),
            "fpr": round(met["fpr"] * 100, 2),
            "f1_score": round(met["f1_score"] * 100, 2),
            "prediction_time": met["prediction_time"]
        }

    # Calcular promedios generales
    n = len(metricas_pct)
    precision_promedio = round(sum(m["accuracy"] for m in metricas_pct.values()) / n, 2)
    recall_promedio = round(sum(m["recall"] for m in metricas_pct.values()) / n, 2)
    tiempo_promedio = round(sum(m["prediction_time"] for m in metricas_pct.values()) / n, 4)

    # Devolver los riesgos
    return {
        "riesgo_lineal": riesgo_lineal,
        "riesgo_poli": riesgo_poli,
        "riesgo_rbf": riesgo_rbf,
        "riesgo_sigmoid": riesgo_sigmoid,
        "riesgo_random_forest": riesgo_random_forest,
        "riesgo_xgboost": riesgo_xgboost,
        "probabilidad_lineal_pct": probabilidad_lineal_pct,
        "probabilidad_poli_pct": probabilidad_poli_pct,
        "probabilidad_rbf_pct": probabilidad_rbf_pct,
        "probabilidad_sigmoid_pct": probabilidad_sigmoid_pct,
        "probabilidad_random_forest_pct": probabilidad_random_forest_pct,
        "probabilidad_xgboost_pct": probabilidad_xgboost_pct,
        "metricas": metricas_pct,
        "precision_promedio": precision_promedio,
        "recall_promedio": recall_promedio,
        "tiempo_promedio": tiempo_promedio,
    }