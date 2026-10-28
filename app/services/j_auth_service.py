from datetime import timedelta
from fastapi import HTTPException, status
from app.core.j_security import j_verificar_password, j_crear_token_acceso
from app.repositories.j_usuarios_repository import j_usuarios_repo
from app.schemas.j_auth_schema import JLoginRequest, JTokenResponse
from app.schemas.j_usuarios_schema import JUsuarioResponse


class JAuthService:
    def j_iniciar_sesion(self, credenciales: JLoginRequest) -> JTokenResponse:
        """
        Autentica un usuario mediante correo y contraseña y genera token JWT (RF01).
        """
        usuario = j_usuarios_repo.j_buscar_por_correo(credenciales.correo)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not j_verificar_password(credenciales.password, usuario.get("password", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if usuario.get("estado") != "ACTIVO":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario se encuentra inactivo. Comuníquese con el administrador."
            )

        # Cargar claims en el token
        datos_token = {
            "sub": usuario["correo"],
            "id_usuario": usuario["id"],
            "rol": usuario["rol"],
            "nombres": usuario["nombres"],
            "apellidos": usuario["apellidos"]
        }
        token = j_crear_token_acceso(datos_token)

        usuario_res = JUsuarioResponse(
            id=usuario["id"],
            identificacion=usuario["identificacion"],
            nombres=usuario["nombres"],
            apellidos=usuario["apellidos"],
            correo=usuario["correo"],
            rol=usuario["rol"],
            estado=usuario["estado"]
        )

        return JTokenResponse(
            access_token=token,
            token_type="bearer",
            rol=usuario["rol"],
            usuario=usuario_res
        )


j_auth_service = JAuthService()
