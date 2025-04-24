import joblib

# Cargar el modelo globalmente
modelo = joblib.load('C:/Users/angel/PycharmProjects/Dengue_Backend/modeloML/modelo_binario_dengue.pkl')

# Función para acceder al modelo
def get_modelo():
    return modelo