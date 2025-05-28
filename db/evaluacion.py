from tortoise import fields
from tortoise.models import Model

class Evaluacion(Model):
    id = fields.IntField(pk=True)
    usuario = fields.ForeignKeyField("models.Usuario", related_name="evaluaciones")
    fecha = fields.DatetimeField(auto_now_add=True)
    riesgo = fields.CharField(max_length=10)  # bajo, medio, alto
    sintomas = fields.JSONField()  # guardar síntomas marcados { "dolor_cabeza_severo": true, ... }
    tiempo_evaluacion = fields.IntField()

    class Meta:
        table = "evaluaciones"
