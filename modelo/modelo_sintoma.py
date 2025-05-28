from typing import Optional
from pydantic import BaseModel

# Modelo para los síntomas del dengue
class FormularioSintomas(BaseModel):
    edad: int
    genero: str
    dias_de_fiebre: int
    dolor_cabeza_severo: bool
    dolor_detras_ojos: bool
    dolor_articular_muscular: bool
    sabor_metalico_boca: bool
    perdida_apetito: bool
    dolor_abdominal: bool
    nauseas_vomitos: bool
    diarrea: bool

    tiempo_evaluacion: Optional[int] = 0  # nuevo campo opcional