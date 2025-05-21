from pathlib import Path
import json
import joblib

# Ruta del archivo actual
ruta_actual = Path(__file__).resolve()

# Subir hasta la raíz del proyecto (dos niveles arriba, porque 'utilidades/utilidades.py')
ruta_base = ruta_actual.parent.parent  # Esto apunta a Dengue_Backend/

# Construir ruta hacia carpeta modeloML
ruta_modelos = ruta_base / 'modeloML'
ruta_metricas = ruta_modelos / 'metricas_modelos.json'

# Cargar modelos
svm_linear = joblib.load(ruta_modelos / 'modelo_svm_lineal_ajustado.pkl')
svm_poly = joblib.load(ruta_modelos / 'modelo_svm_poli_ajustado.pkl')
svm_rbf = joblib.load(ruta_modelos / 'modelo_svm_rbf_ajustado.pkl')
svm_sigmoid = joblib.load(ruta_modelos / 'modelo_svm_sigmoide_ajustado.pkl')
forest = joblib.load(ruta_modelos / 'modelo_random_forest_dengue.pkl')
xgboost = joblib.load(ruta_modelos / 'modelo_xgboost_ajustado.pkl')

# Cargar scaler y PCA
scaler = joblib.load(ruta_modelos / 'scaler.pkl')
pca = joblib.load(ruta_modelos / 'pca.pkl')


# Función para acceder al modelo
def get_modelo():
    return {
        "svm_linear": svm_linear,
        "svm_poly": svm_poly,
        "svm_rbf": svm_rbf,
        "svm_sigmoid": svm_sigmoid,
        "random_forest": forest,
        "xgboost": xgboost
    }

def get_preprocesadores():
    return scaler, pca

# Función para acceder a las métricas
def get_metricas():
    with open(ruta_metricas, "r") as f:
        metricas = json.load(f)
    return metricas