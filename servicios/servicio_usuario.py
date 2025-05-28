import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from tortoise.expressions import Q
from db import Usuario
from modelo import UsuarioRegistro, UsuarioLogin
from utilidades import hash_password, crear_token, verificar_password

def consulta_cmp(cmp_num: str):
    url = 'https://aplicaciones.cmp.org.pe/conoce_a_tu_medico/datos-colegiado.php'
    data = {
        'cmp': cmp_num,
        'appaterno': '',
        'apmaterno': '',
        'nombres': '',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Origin': 'https://aplicaciones.cmp.org.pe',
        'Referer': 'https://aplicaciones.cmp.org.pe/conoce_a_tu_medico/index.php',
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Error en consulta al CMP: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        raise HTTPException(status_code=404, detail="No se encontraron datos para este CMP")

    filas = table.find_all('tr')
    if len(filas) < 2:
        raise HTTPException(status_code=500, detail="La tabla no tiene datos suficientes")

    encabezados = [th.get_text(strip=True) for th in filas[0].find_all(['th', 'td'])]
    valores = [td.get_text(strip=True) for td in filas[1].find_all('td')]

    if len(encabezados) != len(valores):
        raise HTTPException(status_code=500, detail="Encabezados y valores no coinciden")

    resultado = dict(zip(encabezados, valores))

    return {
        'cmp': resultado.get('CMP', cmp_num),
        'apellido_paterno': resultado.get('Ap. Paterno', ''),
        'apellido_materno': resultado.get('Ap. Materno', ''),
        'nombres': resultado.get('Nombres', '')
    }

async def registrar_usuario(usuario: UsuarioRegistro):
    existe = await Usuario.filter(
        Q(correo=usuario.correo) | Q(numero_colegiatura=usuario.numero_colegiatura)
    ).first()

    if existe:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    usuario_dict = usuario.dict()
    usuario_dict["contrasena"] = hash_password(usuario_dict["contrasena"])

    await Usuario.create(**usuario_dict)

    return {"mensaje": "Usuario registrado correctamente"}

async def login_usuario(data: UsuarioLogin):
    usuario = await Usuario.get_or_none(numero_colegiatura=data.numero_colegiatura)
    if not usuario or not verificar_password(data.contrasena, usuario.contrasena):
        raise HTTPException(status_code=401, detail="Número de colegiatura o contraseña incorrectos")

    token = crear_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}