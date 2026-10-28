from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.j_models import JRolUsuario, JEstadoGenerico


class JUsuarioBase(BaseModel):
    identificacion: str = Field(..., min_length=3, max_length=20, description="Número de identificación o documento")
    nombres: str = Field(..., min_length=2, max_length=80, description="Nombres del usuario")
    apellidos: str = Field(..., min_length=2, max_length=80, description="Apellidos del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico único de acceso")
    rol: JRolUsuario = Field(..., description="Rol del usuario: ADMIN, CAJERO o COCINERO")
    estado: JEstadoGenerico = Field(default=JEstadoGenerico.ACTIVO, description="Estado del usuario: ACTIVO o INACTIVO")


class JUsuarioCreate(JUsuarioBase):
    password: str = Field(..., min_length=6, max_length=100, description="Contraseña en texto plano para encriptar con bcrypt")


class JUsuarioUpdate(BaseModel):
    identificacion: Optional[str] = Field(None, min_length=3, max_length=20)
    nombres: Optional[str] = Field(None, min_length=2, max_length=80)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=80)
    correo: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    rol: Optional[JRolUsuario] = None
    estado: Optional[JEstadoGenerico] = None


class JUsuarioResponse(BaseModel):
    """
    Respuesta de usuario.
    Cumple con la regla de negocio RN06: NUNCA se incluye la contraseña.
    """
    id: str
    identificacion: str
    nombres: str
    apellidos: str
    correo: EmailStr
    rol: str
    estado: str

    model_config = ConfigDict(from_attributes=True)
