# app/services/risk_service.py

from models.symptom_model import SymptomForm
import joblib

# Cargar el modelo previamente entrenado (modelo_binario_dengue.pkl)
modelo = joblib.load("D:/Proyecto/modelo_binario_dengue.pkl")


# Función para calcular el riesgo de dengue
def calcular_riesgo(symptoms: SymptomForm):
    # Convertir los síntomas del formulario en una lista de valores 0 y 1
    datos = [
        symptoms.dolor_cabeza_severo,
        symptoms.dolor_detras_ojos,
        symptoms.dolor_articular_muscular,
        symptoms.sabor_metalico_boca,
        symptoms.perdida_apetito,
        symptoms.dolor_abdominal,
        symptoms.nauseas_vomitos,
        symptoms.diarrea
    ]

    # Realizar la predicción usando el modelo
    probabilidad = modelo.predict_proba([datos])[0][1]

    # Determinar el riesgo basado en la probabilidad
    if probabilidad < 0.3:
        return "bajo"
    elif probabilidad < 0.7:
        return "medio"
    else:
        return "alto"
