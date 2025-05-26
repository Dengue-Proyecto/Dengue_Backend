from fastapi import APIRouter, Query
from servicios import consulta_cmp, registrar_usuario, login_usuario
from modelo import UsuarioRegistro, UsuarioLogin

router = APIRouter()

@router.get("/usuario/consulta_cmp")
def ruta_consulta_cmp(cmp_num: str = Query(..., min_length=6, max_length=6, regex=r"^\d{6}$")):
    return consulta_cmp(cmp_num)

@router.post("/usuario/registrar_usuario")
async def ruta_registrar_usuario(usuario: UsuarioRegistro):
    return await registrar_usuario(usuario)

@router.post("/usuario/login")
async def ruta_login_usuario(data: UsuarioLogin):
    return await login_usuario(data)

