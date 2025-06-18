import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from datetime import datetime
from servicios.servicio_riesgo import calcular_riesgo
from modelo import FormularioSintomas


# Fixtures para datos de prueba
@pytest.fixture
def sintomas_basicos():
    """Síntomas básicos para pruebas"""
    return FormularioSintomas(
        edad=25,
        genero="masculino",
        tiempo_inicial=int(datetime.now().timestamp()),
        tiempo_final=int(datetime.now().timestamp()),
        tiempo_evaluacion=5,
        dias_de_fiebre=3,
        dolor_cabeza_severo=True,
        dolor_detras_ojos=False,
        dolor_articular_muscular=True,
        sabor_metalico_boca=False,
        perdida_apetito=True,
        dolor_abdominal=False,
        nauseas_vomitos=False,
        diarrea=False
    )


@pytest.fixture
def sintomas_sin_fiebre():
    """Síntomas sin fiebre"""
    return FormularioSintomas(
        edad=30,
        genero="femenino",
        tiempo_inicial=int(datetime.now().timestamp()),
        tiempo_final=int(datetime.now().timestamp()),
        tiempo_evaluacion=3,
        dias_de_fiebre=0,
        dolor_cabeza_severo=False,
        dolor_detras_ojos=False,
        dolor_articular_muscular=False,
        sabor_metalico_boca=False,
        perdida_apetito=False,
        dolor_abdominal=False,
        nauseas_vomitos=False,
        diarrea=False
    )


@pytest.fixture
def sintomas_todos_positivos():
    """Todos los síntomas positivos"""
    return FormularioSintomas(
        edad=45,
        genero="masculino",
        tiempo_inicial=int(datetime.now().timestamp()),
        tiempo_final=int(datetime.now().timestamp()),
        tiempo_evaluacion=8,
        dias_de_fiebre=7,
        dolor_cabeza_severo=True,
        dolor_detras_ojos=True,
        dolor_articular_muscular=True,
        sabor_metalico_boca=True,
        perdida_apetito=True,
        dolor_abdominal=True,
        nauseas_vomitos=True,
        diarrea=True
    )


@pytest.fixture
def mock_modelos():
    """Mock de los modelos de ML"""
    modelos = {}

    # Crear mocks para cada modelo
    for nombre in ["svm_linear", "svm_poly", "svm_rbf", "svm_sigmoid", "random_forest", "xgboost"]:
        modelo_mock = MagicMock()
        modelo_mock.predict_proba.return_value = np.array([[0.4, 0.6]])  # Probabilidad de riesgo medio
        modelos[nombre] = modelo_mock

    return modelos


@pytest.fixture
def mock_metricas():
    """Mock de las métricas de los modelos"""
    return {
        "svm_linear": {
            "accuracy": 0.85,
            "auc_roc": 0.90,
            "recall": 0.80,
            "specificity": 0.88,
            "fpr": 0.12,
            "f1_score": 0.82,
            "prediction_time": 0.0012
        },
        "svm_poly": {
            "accuracy": 0.87,
            "auc_roc": 0.91,
            "recall": 0.83,
            "specificity": 0.89,
            "fpr": 0.11,
            "f1_score": 0.85,
            "prediction_time": 0.0015
        },
        "svm_rbf": {
            "accuracy": 0.88,
            "auc_roc": 0.92,
            "recall": 0.85,
            "specificity": 0.90,
            "fpr": 0.10,
            "f1_score": 0.87,
            "prediction_time": 0.0018
        },
        "svm_sigmoid": {
            "accuracy": 0.84,
            "auc_roc": 0.89,
            "recall": 0.78,
            "specificity": 0.87,
            "fpr": 0.13,
            "f1_score": 0.81,
            "prediction_time": 0.0014
        },
        "random_forest": {
            "accuracy": 0.90,
            "auc_roc": 0.94,
            "recall": 0.88,
            "specificity": 0.92,
            "fpr": 0.08,
            "f1_score": 0.89,
            "prediction_time": 0.0020
        },
        "xgboost": {
            "accuracy": 0.91,
            "auc_roc": 0.95,
            "recall": 0.89,
            "specificity": 0.93,
            "fpr": 0.07,
            "f1_score": 0.90,
            "prediction_time": 0.0025
        }
    }


@pytest.fixture
def mock_preprocesadores():
    """Mock de los preprocesadores (scaler y PCA)"""
    scaler_mock = MagicMock()
    scaler_mock.transform.return_value = np.array([[0.5]])  # Valor escalado

    pca_mock = MagicMock()
    pca_mock.transform.return_value = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])  # 5 componentes

    return scaler_mock, pca_mock


@pytest.fixture
def mock_gemini_response():
    """Mock de la respuesta de Gemini"""
    response_mock = MagicMock()
    response_mock.text = "Basado en los síntomas presentados, el paciente muestra signos compatibles con dengue. Se recomienda acudir al médico para evaluación y seguimiento."
    return response_mock


# Tests principales
def test_calcular_riesgo_sintomas_basicos(sintomas_basicos, mock_modelos, mock_metricas, mock_preprocesadores,
                                          mock_gemini_response):
    """Test con síntomas básicos - caso más común"""
    scaler_mock, pca_mock = mock_preprocesadores

    with patch('servicios.servicio_riesgo.get_modelo', return_value=mock_modelos), \
            patch('servicios.servicio_riesgo.get_metricas', return_value=mock_metricas), \
            patch('servicios.servicio_riesgo.get_preprocesadores', return_value=(scaler_mock, pca_mock)), \
            patch('servicios.servicio_riesgo.genai.GenerativeModel') as mock_genai:
        # Configurar mock de Gemini
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_gemini_response
        mock_genai.return_value = mock_model

        resultado = calcular_riesgo(sintomas_basicos)

        # Verificar estructura del resultado
        assert isinstance(resultado, dict)

        # Verificar que contiene todos los campos esperados
        campos_esperados = [
            'riesgo_lineal', 'riesgo_poli', 'riesgo_rbf', 'riesgo_sigmoid',
            'riesgo_random_forest', 'riesgo_xgboost',
            'probabilidad_lineal_pct', 'probabilidad_poli_pct', 'probabilidad_rbf_pct',
            'probabilidad_sigmoid_pct', 'probabilidad_random_forest_pct', 'probabilidad_xgboost_pct',
            'probabilidad_random_forest', 'metricas', 'precision_promedio',
            'recall_promedio', 'tiempo_promedio', 'interpretacion'
        ]

        for campo in campos_esperados:
            assert campo in resultado

        # Verificar que los riesgos son válidos
        riesgos_validos = ['bajo', 'medio', 'alto']
        assert resultado['riesgo_lineal'] in riesgos_validos
        assert resultado['riesgo_random_forest'] in riesgos_validos

        # Verificar que las probabilidades están en el rango correcto
        assert 0 <= resultado['probabilidad_lineal_pct'] <= 100
        assert 0 <= resultado['probabilidad_random_forest_pct'] <= 100

        # Verificar que se llamaron los métodos correctos
        scaler_mock.transform.assert_called_once()
        pca_mock.transform.assert_called_once()
        mock_model.generate_content.assert_called_once()


def test_calcular_riesgo_sin_sintomas(sintomas_sin_fiebre, mock_modelos, mock_metricas, mock_preprocesadores,
                                      mock_gemini_response):
    """Test sin síntomas - debería dar riesgo bajo"""
    scaler_mock, pca_mock = mock_preprocesadores

    # Configurar modelos para dar probabilidad baja
    for modelo in mock_modelos.values():
        modelo.predict_proba.return_value = np.array([[0.8, 0.2]])  # Probabilidad baja = riesgo bajo

    with patch('servicios.servicio_riesgo.get_modelo', return_value=mock_modelos), \
            patch('servicios.servicio_riesgo.get_metricas', return_value=mock_metricas), \
            patch('servicios.servicio_riesgo.get_preprocesadores', return_value=(scaler_mock, pca_mock)), \
            patch('servicios.servicio_riesgo.genai.GenerativeModel') as mock_genai:
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_gemini_response
        mock_genai.return_value = mock_model

        resultado = calcular_riesgo(sintomas_sin_fiebre)

        # Verificar que da riesgo bajo
        assert resultado['riesgo_lineal'] == 'bajo'
        assert resultado['riesgo_random_forest'] == 'bajo'
        assert resultado['probabilidad_lineal_pct'] == 20.0


def test_calcular_riesgo_alto(sintomas_todos_positivos, mock_modelos, mock_metricas, mock_preprocesadores,
                              mock_gemini_response):
    """Test con todos los síntomas - debería dar riesgo alto"""
    scaler_mock, pca_mock = mock_preprocesadores

    # Configurar modelos para dar probabilidad alta
    for modelo in mock_modelos.values():
        modelo.predict_proba.return_value = np.array([[0.1, 0.9]])  # Probabilidad alta = riesgo alto

    with patch('servicios.servicio_riesgo.get_modelo', return_value=mock_modelos), \
            patch('servicios.servicio_riesgo.get_metricas', return_value=mock_metricas), \
            patch('servicios.servicio_riesgo.get_preprocesadores', return_value=(scaler_mock, pca_mock)), \
            patch('servicios.servicio_riesgo.genai.GenerativeModel') as mock_genai:
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_gemini_response
        mock_genai.return_value = mock_model

        resultado = calcular_riesgo(sintomas_todos_positivos)

        # Verificar que da riesgo alto
        assert resultado['riesgo_lineal'] == 'alto'
        assert resultado['riesgo_random_forest'] == 'alto'
        assert resultado['probabilidad_lineal_pct'] == 90.0


def test_metricas_conversion_porcentaje(mock_metricas):
    """Test que verifica la conversión de métricas a porcentaje"""
    sintomas_test = FormularioSintomas(
        edad=28,
        genero="masculino",
        tiempo_inicial=int(datetime.now().timestamp()),
        tiempo_final=int(datetime.now().timestamp()),
        tiempo_evaluacion=6,
        dias_de_fiebre=2,
        dolor_cabeza_severo=True,
        dolor_detras_ojos=False,
        dolor_articular_muscular=False,
        sabor_metalico_boca=False,
        perdida_apetito=False,
        dolor_abdominal=False,
        nauseas_vomitos=False,
        diarrea=False
    )

    mock_modelos_simple = {
        "svm_linear": MagicMock(),
        "svm_poly": MagicMock(),
        "svm_rbf": MagicMock(),
        "svm_sigmoid": MagicMock(),
        "random_forest": MagicMock(),
        "xgboost": MagicMock()
    }

    # Configurar todos los modelos para dar la misma probabilidad
    for modelo in mock_modelos_simple.values():
        modelo.predict_proba.return_value = np.array([[0.5, 0.5]])

    scaler_mock = MagicMock()
    scaler_mock.transform.return_value = np.array([[0.5]])
    pca_mock = MagicMock()
    pca_mock.transform.return_value = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])  # 5 componentes como en otros tests

    mock_gemini_response = MagicMock()
    mock_gemini_response.text = "Test response"

    with patch('servicios.servicio_riesgo.get_modelo', return_value=mock_modelos_simple), \
            patch('servicios.servicio_riesgo.get_metricas', return_value=mock_metricas), \
            patch('servicios.servicio_riesgo.get_preprocesadores', return_value=(scaler_mock, pca_mock)), \
            patch('servicios.servicio_riesgo.genai.GenerativeModel') as mock_genai:
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_gemini_response
        mock_genai.return_value = mock_model

        resultado = calcular_riesgo(sintomas_test)

        # Verificar que las métricas se convirtieron a porcentaje
        metricas_resultado = resultado['metricas']['svm_linear']
        assert metricas_resultado['accuracy'] == 85.0  # 0.85 * 100
        assert metricas_resultado['auc_roc'] == 90.0  # 0.90 * 100
        assert metricas_resultado['prediction_time'] == 0.0012  # Sin conversión


def test_error_gemini_api():
    """Test de manejo de errores en la API de Gemini"""
    sintomas_test = FormularioSintomas(
        edad=40,
        genero="femenino",
        tiempo_inicial=int(datetime.now().timestamp()),
        tiempo_final=int(datetime.now().timestamp()),
        tiempo_evaluacion=7,
        dias_de_fiebre=1,
        dolor_cabeza_severo=True,
        dolor_detras_ojos=False,
        dolor_articular_muscular=False,
        sabor_metalico_boca=False,
        perdida_apetito=False,
        dolor_abdominal=False,
        nauseas_vomitos=False,
        diarrea=False
    )

    mock_modelos_simple = {
        "svm_linear": MagicMock(),
        "svm_poly": MagicMock(),
        "svm_rbf": MagicMock(),
        "svm_sigmoid": MagicMock(),
        "random_forest": MagicMock(),
        "xgboost": MagicMock()
    }

    # Configurar todos los modelos
    for modelo in mock_modelos_simple.values():
        modelo.predict_proba.return_value = np.array([[0.5, 0.5]])

    mock_metricas_simple = {}
    for nombre in ["svm_linear", "svm_poly", "svm_rbf", "svm_sigmoid", "random_forest", "xgboost"]:
        mock_metricas_simple[nombre] = {
            "accuracy": 0.85, "auc_roc": 0.90, "recall": 0.80,
            "specificity": 0.88, "fpr": 0.12, "f1_score": 0.82,
            "prediction_time": 0.001
        }

    scaler_mock = MagicMock()
    scaler_mock.transform.return_value = np.array([[0.5]])
    pca_mock = MagicMock()
    pca_mock.transform.return_value = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])  # 5 componentes

    with patch('servicios.servicio_riesgo.get_modelo', return_value=mock_modelos_simple), \
            patch('servicios.servicio_riesgo.get_metricas', return_value=mock_metricas_simple), \
            patch('servicios.servicio_riesgo.get_preprocesadores', return_value=(scaler_mock, pca_mock)), \
            patch('servicios.servicio_riesgo.genai.GenerativeModel') as mock_genai:
        # Simular error en Gemini
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("Error de API")
        mock_genai.return_value = mock_model

        # Verificar que se propaga la excepción
        with pytest.raises(Exception, match="Error de API"):
            calcular_riesgo(sintomas_test)


# Test de integración básica
def test_integracion_completa(sintomas_basicos, mock_modelos, mock_metricas, mock_preprocesadores,
                              mock_gemini_response):
    """Test de integración que verifica todo el flujo"""
    scaler_mock, pca_mock = mock_preprocesadores

    with patch('servicios.servicio_riesgo.get_modelo', return_value=mock_modelos), \
            patch('servicios.servicio_riesgo.get_metricas', return_value=mock_metricas), \
            patch('servicios.servicio_riesgo.get_preprocesadores', return_value=(scaler_mock, pca_mock)), \
            patch('servicios.servicio_riesgo.genai.GenerativeModel') as mock_genai:
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_gemini_response
        mock_genai.return_value = mock_model

        resultado = calcular_riesgo(sintomas_basicos)

        # Verificar que se ejecutaron todos los pasos
        scaler_mock.transform.assert_called_once()
        pca_mock.transform.assert_called_once()

        # Verificar que se llamaron todos los modelos
        for modelo in mock_modelos.values():
            modelo.predict_proba.assert_called_once()

        # Verificar que se generó la interpretación
        mock_model.generate_content.assert_called_once()

        # Verificar que el resultado es completo y coherente
        assert isinstance(resultado, dict)
        assert len(resultado) == 18  # Todos los campos esperados
        assert resultado['interpretacion'] == mock_gemini_response.text