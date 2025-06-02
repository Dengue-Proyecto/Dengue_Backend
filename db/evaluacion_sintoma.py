from tortoise import fields
from tortoise.models import Model

class EvaluacionSintoma(Model):
    id = fields.IntField(pk=True)
    evaluacion = fields.ForeignKeyField("models.Evaluacion", related_name="evaluacion_sintomas")
    sintoma = fields.ForeignKeyField("models.Sintoma", related_name="evaluacion_sintomas")

    class Meta:
        table = "evaluacion_sintomas"
        unique_together = ("evaluacion", "sintoma")