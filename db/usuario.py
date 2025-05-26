from tortoise import fields
from tortoise.models import Model

class Usuario(Model):
    id = fields.IntField(pk=True)
    numero_colegiatura = fields.CharField(max_length=6, unique=True)
    nombres = fields.CharField(max_length=100)
    apellido_paterno = fields.CharField(max_length=50)
    apellido_materno = fields.CharField(max_length=50)
    correo = fields.CharField(max_length=100, unique=True)
    contrasena = fields.CharField(max_length=255)

    class Meta:
        table = "usuarios"