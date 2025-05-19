import joblib
import json

# Cargar el modelo globalmente
svm_linear = joblib.load('C:/Users/angel/PycharmProjects/Dengue_Backend/modeloML/modelo_svm_lineal_ajustado.pkl')
svm_poly = joblib.load('C:/Users/angel/PycharmProjects/Dengue_Backend/modeloML/modelo_svm_poli_ajustado.pkl')
svm_rbf = joblib.load('C:/Users/angel/PycharmProjects/Dengue_Backend/modeloML/modelo_svm_rbf_ajustado.pkl')
svm_sigmoid = joblib.load('C:/Users/angel/PycharmProjects/Dengue_Backend/modeloML/modelo_svm_sigmoide_ajustado.pkl')
forest = joblib.load('C:/Users/angel/PycharmProjects/Dengue_Backend/modeloML/modelo_random_forest_dengue.pkl')

# Ruta al archivo JSON con métricas
ruta_metricas = 'C:/Users/angel/PycharmProjects/Dengue_Backend/modeloML/metricas_modelos.json'

# Función para acceder al modelo
def get_modelo():
    return {
        "svm_linear": svm_linear,
        "svm_poly": svm_poly,
        "svm_rbf": svm_rbf,
        "svm_sigmoid": svm_sigmoid,
        "random_forest": forest,
    }

# Función para acceder a las métricas
def get_metricas():
    with open(ruta_metricas, "r") as f:
        metricas = json.load(f)
    return metricas