from tortoise import fields
from tortoise.models import Model

class Sintoma(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=50, unique=True)  # ej: "dolor_cabeza_severo"

    class Meta:
        table = "sintomas"