import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException
from servicios import consulta_cmp, registrar_usuario, login_usuario
from modelo import UsuarioRegistro, UsuarioLogin
from utilidades import hash_password

# Mock para requests.post
@pytest.fixture
def mock_requests_post():
    with patch('servicios.servicio_usuario.requests.post') as mock_post:
        yield mock_post

# Fixtures para datos de prueba
@pytest.fixture
def usuario_registro():
    return UsuarioRegistro(
        correo="usuario@lunaweb.com",
        numero_colegiatura="123456",
        contrasena="12345",
        nombres="Juan Juanito",
        apellido_paterno="Abanto",
        apellido_materno="Perez"
    )


@pytest.fixture
def usuario_login():
    return UsuarioLogin(numero_colegiatura="123456", contrasena="12345")

# Tests de consulta_cmp
def test_consulta_cmp_datos_completos(mock_requests_post):
    """Test con todos los campos llenos"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '''
    <html><body>
        <table>
            <tr>
                <th>CMP</th><th>Ap. Paterno</th><th>Ap. Materno</th><th>Nombres</th>
            </tr>
            <tr>
                <td>12345</td><td>García</td><td>López</td><td>Juan Carlos</td>
            </tr>
        </table>
    </body></html>
    '''
    mock_requests_post.return_value = mock_response

    resultado = consulta_cmp("12345")

    assert resultado['cmp'] == "12345"
    assert resultado['apellido_paterno'] == "García"
    assert resultado['apellido_materno'] == "López"
    assert resultado['nombres'] == "Juan Carlos"


def test_consulta_cmp_sin_tabla(mock_requests_post):
    """Test cuando no se encuentra tabla en la respuesta"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<html><body><p>No hay datos</p></body></html>'
    mock_requests_post.return_value = mock_response

    with pytest.raises(HTTPException) as exc_info:
        consulta_cmp("12345")
    assert exc_info.value.status_code == 404


def test_consulta_cmp_tabla_incompleta(mock_requests_post):
    """Test cuando la tabla no tiene suficientes filas"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<html><body><table><tr><th>CMP</th></tr></table></body></html>'
    mock_requests_post.return_value = mock_response

    with pytest.raises(HTTPException) as exc_info:
        consulta_cmp("12345")
    assert exc_info.value.status_code == 500


def test_consulta_cmp_error(mock_requests_post):
    """Test cuando hay error en la solicitud HTTP"""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_requests_post.return_value = mock_response

    with pytest.raises(HTTPException) as exc_info:
        consulta_cmp("12345")
    assert exc_info.value.status_code == 500


# Tests de registrar_usuario - CORREGIDOS
@pytest.mark.asyncio
async def test_registrar_usuario_exitoso(usuario_registro):
    """Test de registro exitoso"""
    # Mock para la consulta de usuario existente
    with patch('servicios.servicio_usuario.Usuario.filter') as mock_filter:
        # Crear un mock del QuerySet que retorna None en first()
        mock_queryset = AsyncMock()
        mock_queryset.first = AsyncMock(return_value=None)
        mock_filter.return_value = mock_queryset

        # Mock para la creación del usuario
        with patch('servicios.servicio_usuario.Usuario.create', new_callable=AsyncMock) as mock_create:
            mock_create.return_value = None

            response = await registrar_usuario(usuario_registro)

            # Verificaciones
            assert response == {"mensaje": "Usuario registrado correctamente"}
            mock_filter.assert_called_once()
            mock_create.assert_called_once()

            # Verificar que los datos se pasaron correctamente
            call_args = mock_create.call_args[1]  # kwargs
            assert call_args['correo'] == usuario_registro.correo
            assert call_args['numero_colegiatura'] == usuario_registro.numero_colegiatura
            # Verificar que la contraseña fue hasheada
            assert call_args['contrasena'] != usuario_registro.contrasena


@pytest.mark.asyncio
async def test_registrar_usuario_ya_existente(usuario_registro):
    """Test cuando el usuario ya existe"""
    # Mock para la consulta de usuario existente
    with patch('servicios.servicio_usuario.Usuario.filter') as mock_filter:
        # Crear un mock del QuerySet que retorna un usuario existente
        usuario_existente = MagicMock()
        mock_queryset = AsyncMock()
        mock_queryset.first = AsyncMock(return_value=usuario_existente)
        mock_filter.return_value = mock_queryset

        with pytest.raises(HTTPException) as exc_info:
            await registrar_usuario(usuario_registro)

        assert exc_info.value.status_code == 400
        assert "Usuario ya registrado" in str(exc_info.value.detail)


# Tests de login_usuario
@pytest.mark.asyncio
async def test_login_usuario_exitoso(usuario_login):
    """Test de login exitoso"""
    with patch('servicios.servicio_usuario.Usuario.get_or_none', new_callable=AsyncMock) as mock_get:
        # Mock del usuario encontrado
        usuario_mock = MagicMock()
        usuario_mock.id = 1
        usuario_mock.contrasena = hash_password(usuario_login.contrasena)
        mock_get.return_value = usuario_mock

        with patch('servicios.servicio_usuario.verificar_password') as mock_verificar:
            mock_verificar.return_value = True

            with patch('servicios.servicio_usuario.crear_token') as mock_token:
                mock_token.return_value = "mocked_token"

                response = await login_usuario(usuario_login)

                assert "access_token" in response
                assert response["token_type"] == "bearer"
                assert response["access_token"] == "mocked_token"

                # Verificaciones de llamadas
                mock_get.assert_called_once_with(numero_colegiatura=usuario_login.numero_colegiatura)
                mock_verificar.assert_called_once()
                mock_token.assert_called_once()


@pytest.mark.asyncio
async def test_login_usuario_no_encontrado(usuario_login):
    """Test cuando el usuario no existe"""
    with patch('servicios.servicio_usuario.Usuario.get_or_none', new_callable=AsyncMock) as mock_get:
        mock_get.return_value = None  # Usuario no encontrado

        with pytest.raises(HTTPException) as exc_info:
            await login_usuario(usuario_login)

        assert exc_info.value.status_code == 401
        assert "Número de colegiatura o contraseña incorrectos" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_login_usuario_contrasena_incorrecta(usuario_login):
    """Test cuando la contraseña es incorrecta"""
    with patch('servicios.servicio_usuario.Usuario.get_or_none', new_callable=AsyncMock) as mock_get:
        # Mock del usuario encontrado
        usuario_mock = MagicMock()
        usuario_mock.id = 1
        usuario_mock.contrasena = hash_password("otra_contrasena")
        mock_get.return_value = usuario_mock

        with patch('servicios.servicio_usuario.verificar_password') as mock_verificar:
            mock_verificar.return_value = False  # Contraseña incorrecta

            with pytest.raises(HTTPException) as exc_info:
                await login_usuario(usuario_login)

            assert exc_info.value.status_code == 401
            assert "Número de colegiatura o contraseña incorrectos" in str(exc_info.value.detail)