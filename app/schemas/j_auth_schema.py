from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.j_models import JRolUsuario
from app.schemas.j_usuarios_schema import JUsuarioResponse


class JLoginRequest(BaseModel):
    correo: EmailStr = Field(..., description="Correo del usuario para iniciar sesión")
    password: str = Field(..., description="Contraseña de acceso")


class JTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
    usuario: JUsuarioResponse


class JRegistroRequest(BaseModel):
    identificacion: str = Field(..., min_length=3, max_length=20)
    nombres: str = Field(..., min_length=2, max_length=80)
    apellidos: str = Field(..., min_length=2, max_length=80)
    correo: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    rol: JRolUsuario = JRolUsuario.CAJERO


class JTokenPayload(BaseModel):
    sub: Optional[str] = None
    id_usuario: Optional[str] = None
    rol: Optional[str] = None
    exp: Optional[int] = None
