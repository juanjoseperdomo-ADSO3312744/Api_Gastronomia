from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from app.models.j_models import JTipoCliente, JEstadoGenerico


class JClienteBase(BaseModel):
    identificacion: str = Field(..., min_length=3, max_length=20, description="Número de documento de identidad del cliente")
    nombres: str = Field(..., min_length=2, max_length=80, description="Nombres del cliente")
    apellidos: str = Field(..., min_length=2, max_length=80, description="Apellidos del cliente")
    telefono: Optional[str] = Field(default="", max_length=30, description="Teléfono de contacto")
    correo: Optional[EmailStr] = Field(default=None, description="Correo electrónico del cliente")
    tipo_cliente: JTipoCliente = Field(..., description="Tipo de cliente: APRENDIZ, INSTRUCTOR, FUNCIONARIO o EXTERNO")
    estado: JEstadoGenerico = Field(default=JEstadoGenerico.ACTIVO, description="Estado del cliente: ACTIVO o INACTIVO")


class JClienteCreate(JClienteBase):
    pass


class JClienteUpdate(BaseModel):
    identificacion: Optional[str] = Field(None, min_length=3, max_length=20)
    nombres: Optional[str] = Field(None, min_length=2, max_length=80)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=80)
    telefono: Optional[str] = Field(None, max_length=30)
    correo: Optional[EmailStr] = None
    tipo_cliente: Optional[JTipoCliente] = None
    estado: Optional[JEstadoGenerico] = None


class JClienteResponse(BaseModel):
    id: str
    identificacion: str
    nombres: str
    apellidos: str
    telefono: Optional[str] = ""
    correo: Optional[str] = None
    tipo_cliente: str
    estado: str

    model_config = ConfigDict(from_attributes=True)
