# 🦟 Dengue Backend - Sistema de Evaluación de Riesgo

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/Google%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google AI">
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest">
</div>

<br>

Backend para el sistema de evaluación de riesgo de dengue utilizando inteligencia artificial y machine learning.

## 🚀 Características

- **API RESTful** con FastAPI
- **Autenticación JWT** segura
- **Machine Learning** para predicción de riesgo de dengue
- **Integración con CMP** (Colegio Médico del Perú)
- **Base de datos MySQL** con ORM asíncrono
- **Integración con Google Gemini AI**
- **Tests automatizados** con pytest

## 🛠️ Tecnologías

- **FastAPI** - Framework web moderno para APIs
- **Python** - Lenguaje de programación
- **Tortoise ORM** - ORM asíncrono
- **MySQL** - Base de datos
- **Scikit-learn** - Machine Learning
- **JWT** - Autenticación
- **Google Generative AI** - IA generativa
- **Uvicorn** - Servidor ASGI

## 📋 Requisitos Previos

- Python 3.8+
- MySQL
- Cuenta de Google Cloud (para Gemini AI)

## 🔧 Instalación

1. **Clona el repositorio**
```bash
git clone https://github.com/Dengue-Proyecto/Dengue_Backend.git
cd Dengue_Backend
```

2. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

3. **Configura las variables de entorno**
Crea un archivo `.env` con:
```env
DATABASE_URL=mysql://usuario:contraseña@localhost:3306/dengue_db
SECRET_KEY=tu_clave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_GEMINI=tu_api_key_de_gemini
```

4. **Ejecuta la aplicación**
```bash
uvicorn main:app --reload
```

## 📚 Endpoints Principales

### Autenticación
- `POST /usuario/registrar_usuario` - Registro de usuarios
- `POST /usuario/login` - Inicio de sesión
- `POST /auth/token` - Token OAuth2

### Evaluación de Riesgo
- `POST /evaluar_riesgo` - Evaluar riesgo de dengue
- `GET /mis_evaluaciones` - Obtener evaluaciones del usuario

### Utilidades
- `GET /usuario/consulta_cmp` - Consultar datos del CMP

## 🧪 Testing

```bash
pytest
# o para tests específicos
pytest
```

## 🤖 Machine Learning

El sistema utiliza múltiples algoritmos de ML para predecir el riesgo de dengue:
- **Random Forest**
- **XGBoost**
- **4 Kernels de Regresión Logística**

Los resultados se clasifican en:
- **Bajo riesgo**: < 30%
- **Riesgo medio**: 30-70%
- **Alto riesgo**: > 70%

## 🔒 Seguridad

- Autenticación JWT
- Contraseñas encriptadas con bcrypt
- Validación de datos con Pydantic
- Configuración CORS para frontend

## 🚀 Despliegue

La aplicación está configurada para trabajar con:
- **Frontend Angular** en `localhost:4200`
- **Producción** en `https://riesgodengue.netlify.app`
