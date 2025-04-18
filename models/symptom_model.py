from pydantic import BaseModel

# Modelo para los síntomas del dengue
class SymptomForm(BaseModel):
    dolor_cabeza_severo: bool
    dolor_detras_ojos: bool
    dolor_articular_muscular: bool
    sabor_metalico_boca: bool
    perdida_apetito: bool
    dolor_abdominal: bool
    nauseas_vomitos: bool
    diarrea: bool

    class Config:
        # Configuración para que los datos booleanos sean validados como 'true'/'false'
        use_enum_values = True