from tortoise import fields
from tortoise.models import Model

class Evaluacion(Model):
    id = fields.IntField(pk=True)
    usuario = fields.ForeignKeyField("models.Usuario", related_name="evaluaciones")
    fecha = fields.DatetimeField(auto_now_add=True)
    riesgo = fields.CharField(max_length=10)  # 'bajo', 'medio', 'alto'
    probabilidad = fields.FloatField()  # Para almacenar la probabilidad calculada (ejemplo: 0.265)
    tiempo_inicial = fields.DatetimeField()
    tiempo_final = fields.DatetimeField()
    riesgo_real = fields.CharField(max_length=10, null=True)  # 'bajo', 'medio', 'alto', 'negativo' - diagnosticado por doctor

    evaluacion_sintomas: fields.ReverseRelation["EvaluacionSintoma"]  # relación inversa

    class Meta:
        table = "evaluaciones"