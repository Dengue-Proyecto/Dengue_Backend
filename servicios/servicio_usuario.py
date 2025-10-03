import time
import logging
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fastapi import HTTPException
from tortoise.expressions import Q
from db import Usuario
from modelo import UsuarioRegistro, UsuarioLogin
from utilidades import hash_password, crear_tokens, verificar_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def consulta_cmp(cmp_num: str):
    """
    Consulta información de un médico en el CMP usando Selenium
    """
    driver = None

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36')

        logger.info("Iniciando ChromeDriver...")
        # Detectar si estoy en EC2 (ejemplo: por variable de entorno)
        if os.environ.get("EC2_ENV", "false") == "true":
            service = Service("/usr/bin/chromedriver")
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Scripts anti-detección
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
        })
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        logger.info(f"Consultando CMP: {cmp_num}")

        # Navegar
        driver.get('https://aplicaciones.cmp.org.pe/conoce_a_tu_medico/index.php')
        logger.info("Página cargada")

        # Esperar a que cargue completamente
        time.sleep(3)

        # Esperar a que grecaptcha esté disponible
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return typeof grecaptcha !== 'undefined' && grecaptcha.ready !== undefined")
        )
        logger.info("reCAPTCHA cargado")

        # Llenar el formulario
        cmp_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'cmp'))
        )
        cmp_input.clear()
        cmp_input.send_keys(cmp_num)
        logger.info(f"Campo CMP llenado: {cmp_num}")

        # MeTODO 1: Ejecutar directamente el script que genera el token y envía el form
        logger.info("Ejecutando reCAPTCHA y enviando formulario...")

        script = """
        return new Promise((resolve, reject) => {
            grecaptcha.ready(function() {
                grecaptcha.execute('6LcYiNwrAAAAAB2vkiot46ogkFJj0MRakLVZTQRa', 
                    { action: 'colegiados_busqueda' })
                .then(function(token) {
                    document.getElementById('g-recaptcha-response').value = token;
                    document.getElementById('form-colegiados').submit();
                    resolve(true);
                })
                .catch(function(error) {
                    reject(error);
                });
            });
        });
        """

        try:
            driver.execute_script(script)
            logger.info("Formulario enviado con reCAPTCHA")
        except Exception as e:
            logger.error(f"Error al ejecutar reCAPTCHA: {e}")
            raise HTTPException(status_code=503, detail="Error al validar reCAPTCHA")

        # Esperar a que cambie la URL o aparezca contenido nuevo
        time.sleep(5)

        # La página debe haber cambiado o mostrar resultados
        current_url = driver.current_url
        logger.info(f"URL actual: {current_url}")

        # Verificar si hay un mensaje de error de reCAPTCHA
        page_text = driver.page_source.lower()
        if 'recaptcha fallida' in page_text or 'validación recaptcha' in page_text:
            logger.error("reCAPTCHA falló en el backend")
            raise HTTPException(
                status_code=503,
                detail="El servidor rechazó la validación reCAPTCHA. Este endpoint no puede automatizarse."
            )

        # Buscar la tabla en la página actual o en iframe
        table_element = None

        # Intentar en la página principal
        try:
            table_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'table'))
            )
            logger.info("Tabla encontrada en página principal")
        except:
            logger.info("No hay tabla en página principal, buscando iframe...")

        # Si no está en la página principal, buscar en iframe
        if not table_element:
            try:
                iframes = driver.find_elements(By.TAG_NAME, 'iframe')
                logger.info(f"Iframes encontrados: {len(iframes)}")

                for idx, iframe in enumerate(iframes):
                    try:
                        driver.switch_to.frame(iframe)
                        table_element = driver.find_element(By.TAG_NAME, 'table')
                        logger.info(f"Tabla encontrada en iframe {idx}")
                        break
                    except:
                        driver.switch_to.default_content()
                        continue
            except Exception as e:
                logger.error(f"Error buscando en iframes: {e}")

        if not table_element:
            # Guardar HTML para debug
            with open('debug/respuesta_final.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            logger.error("No se encontró tabla. HTML guardado en debug/respuesta_final.html")
            raise HTTPException(status_code=404, detail="No se encontraron datos para este CMP")

        # Parsear con BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table')

        if not table:
            raise HTTPException(status_code=404, detail="No se encontraron datos")

        filas = table.find_all('tr')
        if len(filas) < 2:
            raise HTTPException(status_code=404, detail="No hay datos disponibles")

        # Extraer datos
        encabezados = [th.get_text(strip=True) for th in filas[0].find_all(['th', 'td'])]
        valores = [td.get_text(strip=True) for td in filas[1].find_all('td')]

        logger.info(f"Encabezados: {encabezados}")
        logger.info(f"Valores: {valores}")

        if len(encabezados) != len(valores):
            raise HTTPException(status_code=500, detail="Error al procesar datos")

        resultado = dict(zip(encabezados, valores))

        logger.info("✅ Consulta exitosa")

        return {
            'cmp': resultado.get('CMP', cmp_num),
            'apellido_paterno': resultado.get('Ap. Paterno', ''),
            'apellido_materno': resultado.get('Ap. Materno', ''),
            'nombres': resultado.get('Nombres', '')
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error al consultar CMP: {str(e)}")

    finally:
        if driver:
            try:
                driver.quit()
                logger.info("Driver cerrado")
            except:
                pass

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