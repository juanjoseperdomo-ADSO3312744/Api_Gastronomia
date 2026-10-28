from fastapi import APIRouter, Depends, status
from app.schemas.j_auth_schema import JLoginRequest, JTokenResponse, JRegistroRequest
from app.schemas.j_usuarios_schema import JUsuarioResponse, JUsuarioCreate
from app.services.j_auth_service import j_auth_service
from app.services.j_usuarios_service import j_usuarios_service
from app.core.j_security import j_obtener_usuario_actual, j_requiere_roles

j_auth_router = APIRouter(prefix="/auth", tags=["Autenticación"])


@j_auth_router.post(
    "/login",
    response_model=JTokenResponse,
    summary="Iniciar sesión y obtener token JWT",
    description="Endpoint público para autenticar credenciales de usuario (correo y contraseña) y obtener token Bearer JWT con su rol (RF01)."
)
def j_login(credenciales: JLoginRequest):
    return j_auth_service.j_iniciar_sesion(credenciales)


@j_auth_router.post(
    "/registro",
    response_model=JUsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario (Solo ADMIN)",
    description="Permite a un usuario con rol ADMIN crear una nueva cuenta de acceso en el sistema."
)
def j_registro(
    datos: JRegistroRequest,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN"]))
):
    usuario_crear = JUsuarioCreate(
        identificacion=datos.identificacion,
        nombres=datos.nombres,
        apellidos=datos.apellidos,
        correo=datos.correo,
        password=datos.password,
        rol=datos.rol
    )
    return j_usuarios_service.j_crear_usuario(usuario_crear)


@j_auth_router.get(
    "/perfil",
    response_model=JUsuarioResponse,
    summary="Consultar perfil del usuario autenticado",
    description="Retorna la información básica del usuario autenticado a partir de su token JWT. La contraseña nunca se incluye (RN06)."
)
def j_perfil(usuario_actual: dict = Depends(j_obtener_usuario_actual)):
    return usuario_actual
