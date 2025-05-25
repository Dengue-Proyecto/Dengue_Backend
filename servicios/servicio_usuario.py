import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from modelo import UsuarioRegistro

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

# Simulación de almacenamiento en memoria (usar DB en producción)
usuarios_registrados = []

def registrar_usuario(usuario: UsuarioRegistro) -> bool:
    # Validar si ya existe usuario con ese correo o colegiatura (ejemplo)
    for u in usuarios_registrados:
        if u.correo == usuario.correo or u.numero_colegiatura == usuario.numero_colegiatura:
            return False  # Ya existe

    # Guardar usuario (en DB o memoria)
    usuarios_registrados.append(usuario)
    return True