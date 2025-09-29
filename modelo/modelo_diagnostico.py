from pydantic import BaseModel

class ActualizarDiagnostico(BaseModel):
    riesgo_real: str  # 'bajo', 'medio', 'alto', 'negativo'
