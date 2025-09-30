import requests
import os
from bs4 import BeautifulSoup
from fastapi import HTTPException
from tortoise.expressions import Q
from db import Usuario
from modelo import UsuarioRegistro, UsuarioLogin
from utilidades import hash_password, crear_tokens, verificar_password

def consulta_cmp(cmp_num: str):
    # Obtener cookies dinámicamente de las variables de entorno
    o9g0 = os.getenv('o9$g0$t1750221152$j60$l0$h0')
    o11g1 = os.getenv('o11$g1$t1750222541$j60$l0$h0')

    cookies = {
        '_ga': 'GA1.1.511452197.1747891703',
        '_ga_GK24WGPPTG': f"GS2.1.s1750221152{o9g0}",
        '_ga_74HE66R4YE': f"GS2.1.s1750221153{o11g1}",
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Origin': 'https://aplicaciones.cmp.org.pe',
        'Referer': 'https://aplicaciones.cmp.org.pe/conoce_a_tu_medico/index.php',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'cmp': cmp_num,
        'appaterno': '',
        'apmaterno': '',
        'nombres': '',
    }

    # Hacer la solicitud POST
    response = requests.post('https://aplicaciones.cmp.org.pe/conoce_a_tu_medico/datos-colegiado.php',
                             cookies=cookies, headers=headers, data=data, verify=False)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Error en consulta al CMP: {response.status_code}")

    # Procesar la respuesta con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        raise HTTPException(status_code=404, detail="No se encontraron datos para este CMP")

    filas = table.find_all('tr')
    if len(filas) < 2:
        raise HTTPException(status_code=500, detail="La tabla no tiene datos suficientes")

    # Extraer encabezados y valores
    encabezados = [th.get_text(strip=True) for th in filas[0].find_all(['th', 'td'])]
    valores = [td.get_text(strip=True) for td in filas[1].find_all('td')]

    if len(encabezados) != len(valores):
        raise HTTPException(status_code=500, detail="Encabezados y valores no coinciden")

    # Construir el diccionario de resultados
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

    usuario_dict = usuario.model_dump()
    usuario_dict["contrasena"] = hash_password(usuario_dict["contrasena"])

    await Usuario.create(**usuario_dict)

    return {"mensaje": "Usuario registrado correctamente"}

async def login_usuario(data: UsuarioLogin):
    usuario = await Usuario.get_or_none(numero_colegiatura=data.numero_colegiatura)
    if not usuario or not verificar_password(data.contrasena, usuario.contrasena):
        raise HTTPException(status_code=401, detail="Número de colegiatura o contraseña incorrectos")

    tokens = crear_tokens(str(usuario.id))
    return {**tokens}