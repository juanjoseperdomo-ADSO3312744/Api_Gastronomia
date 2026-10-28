from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.j_config import j_settings
from app.database.j_conexion_mongo import j_obtener_bd, j_serializar_doc, j_validar_objectid

# Esquema de autenticación HTTP Bearer para Swagger UI y peticiones autenticadas
# Permite ingresar únicamente el token JWT en el botón Authorize de Swagger UI (/docs)
j_bearer_esquema = HTTPBearer(
    bearerFormat="JWT",
    auto_error=False,
    description="Ingrese únicamente su token JWT Bearer (sin prefijo Bearer)."
)

# Alias de compatibilidad hacia atrás
j_oauth2_esquema = j_bearer_esquema


def j_hashear_password(password: str) -> str:
    """
    Cifra una contraseña de texto plano utilizando el algoritmo seguro bcrypt.
    Cumple con la regla de negocio RN06.
    """
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash_bytes.decode("utf-8")


def j_verificar_password(plain_password: str, hashed_password: str) -> bool:
    """
    Comprueba si una contraseña en texto plano coincide con el hash almacenado en bcrypt.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def j_crear_token_acceso(datos: dict, expira_delta: Optional[timedelta] = None) -> str:
    """
    Genera un token JWT firmado con la clave secreta y tiempo de expiración.
    """
    para_codificar = datos.copy()
    ahora = datetime.now(timezone.utc)
    if expira_delta:
        expiracion = ahora + expira_delta
    else:
        expiracion = ahora + timedelta(minutes=j_settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    para_codificar.update({
        "exp": expiracion,
        "iat": ahora
    })
    token_codificado = jwt.encode(
        para_codificar,
        j_settings.SECRET_KEY,
        algorithm=j_settings.ALGORITHM
    )
    return token_codificado


def j_decodificar_token(token: str) -> dict:
    """
    Decodifica y valida la firma y vigencia de un token JWT.
    """
    try:
        payload = jwt.decode(
            token,
            j_settings.SECRET_KEY,
            algorithms=[j_settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido o ha expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def j_obtener_usuario_actual(
    credenciales: Optional[HTTPAuthorizationCredentials] = Depends(j_bearer_esquema)
) -> Dict[str, Any]:
    """
    Dependencia de FastAPI para obtener y validar el usuario autenticado a partir del JWT Bearer.
    Swagger UI únicamente solicita el token JWT en el formulario de autorización.
    """
    if credenciales is None or not credenciales.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionaron credenciales de autenticación.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credenciales.credentials.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    payload = j_decodificar_token(token)
    correo: Optional[str] = payload.get("sub")
    if correo is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas (falta subject en el token).",
            headers={"WWW-Authenticate": "Bearer"},
        )

    bd = j_obtener_bd()
    usuario = bd["usuarios"].find_one({"correo": correo})
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario autenticado no existe en la base de datos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if usuario.get("estado") != "ACTIVO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario se encuentra inactivo en el sistema.",
        )

    return j_serializar_doc(usuario)


def j_requiere_roles(roles_permitidos: List[str]):
    """
    Fábrica de dependencias para validar el control de acceso basado en roles (RBAC).
    Retorna 403 Forbidden si el rol del usuario no está en la lista permitida.
    """
    async def _verificador_rol(usuario_actual: Dict[str, Any] = Depends(j_obtener_usuario_actual)):
        rol_usuario = usuario_actual.get("rol")
        if rol_usuario not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los siguientes roles: {', '.join(roles_permitidos)}. Su rol actual es: {rol_usuario}."
            )
        return usuario_actual

    return _verificador_rol
