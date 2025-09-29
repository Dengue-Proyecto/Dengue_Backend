from pydantic import BaseModel

class ActualizarDiagnostico(BaseModel):
    resultado: str  # 'bajo', 'medio', 'alto', 'negativo'
