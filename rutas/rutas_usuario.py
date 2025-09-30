from fastapi import APIRouter, Query, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from servicios import consulta_cmp, registrar_usuario, login_usuario
from modelo import UsuarioRegistro, UsuarioLogin
from utilidades import crear_tokens, decodificar_token

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

# Endpoint para OAuth2/Swagger (Form data)
@router.post("/auth/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    data = UsuarioLogin(
        numero_colegiatura=form_data.username,
        contrasena=form_data.password
    )
    return await login_usuario(data)


@router.post("/auth/refresh")
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    """
    Endpoint para renovar tokens usando el refresh token.
    Esto simula la expiración por inactividad: cada vez que el usuario
    hace una petición, se renuevan ambos tokens con nuevos tiempos de expiración.

    Body esperado: {"refresh_token": "tu_refresh_token_aqui"}
    """
    try:
        # Validar el refresh token
        payload = decodificar_token(refresh_token, token_type="refresh")
        usuario_id = payload.get("sub")

        if not usuario_id:
            raise HTTPException(status_code=401, detail="Refresh token inválido")

        # Crear nuevos tokens (sliding window - se resetea el tiempo de inactividad)
        nuevos_tokens = crear_tokens(usuario_id)

        return nuevos_tokens

    except HTTPException as e:
        # Si el refresh token expiró, el usuario debe iniciar sesión nuevamente
        if "expirado" in e.detail.lower():
            raise HTTPException(
                status_code=401,
                detail="Sesión expirada por inactividad. Por favor, inicia sesión nuevamente."
            )
        raise e