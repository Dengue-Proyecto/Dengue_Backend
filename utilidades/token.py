import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def crear_access_token(data: dict):
    """Crea un access token de corta duración"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def crear_refresh_token(data: dict):
    """Crea un refresh token de larga duración que se renueva con cada actividad"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def crear_tokens(usuario_id: str):
    """Crea ambos tokens (access y refresh) para un usuario"""
    data = {"sub": usuario_id}
    access_token = crear_access_token(data)
    refresh_token = crear_refresh_token(data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def decodificar_token(token: str, token_type: str = "access"):
    """Decodifica y valida un token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verificar que el tipo de token coincida
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=401,
                detail=f"Token inválido: se esperaba tipo '{token_type}'"
            )

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expirado - por favor, inicia sesión nuevamente"
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    """Obtiene el usuario actual desde el access token"""
    payload = decodificar_token(token, token_type="access")
    usuario_id = payload.get("sub")

    if not usuario_id:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return usuario_id

# Función legacy mantenida para compatibilidad (ahora llama a crear_tokens)
def crear_token(data: dict, expires_delta: timedelta = None):
    """Función legacy - usa crear_tokens() en su lugar"""
    usuario_id = data.get("sub")
    return crear_tokens(usuario_id)["access_token"]