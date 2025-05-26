from pydantic import BaseModel,EmailStr

class UsuarioRegistro(BaseModel):
    numero_colegiatura: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    correo: EmailStr
    contrasena: str

class UsuarioLogin(BaseModel):
    numero_colegiatura: str
    contrasena: str