from fastapi import APIRouter, Query
from servicios import consulta_cmp
from servicios import registrar_usuario
from modelo import UsuarioRegistro

router = APIRouter()

@router.get("/usuario/consulta_cmp")
def ruta_consulta_cmp(cmp_num: str = Query(..., min_length=6, max_length=6, regex=r"^\d{6}$")):
    return consulta_cmp(cmp_num)

@router.post("/usuario/registrar_usuario")
def ruta_registrar_usuario(usuario: UsuarioRegistro):
    # Llamar función para guardar usuario
    registrar_usuario(usuario)

