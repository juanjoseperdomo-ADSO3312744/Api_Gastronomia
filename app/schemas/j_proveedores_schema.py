from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from app.models.j_models import JEstadoGenerico


class JProveedorBase(BaseModel):
    nit: str = Field(..., min_length=3, max_length=20, description="NIT o documento de identificación único del proveedor")
    razon_social: str = Field(..., min_length=2, max_length=120, description="Razón social o nombre comercial")
    telefono: Optional[str] = Field(default="", max_length=30, description="Teléfono de contacto")
    correo: Optional[EmailStr] = Field(default=None, description="Correo electrónico del proveedor")
    direccion: Optional[str] = Field(default="", max_length=150, description="Dirección física")
    estado: JEstadoGenerico = Field(default=JEstadoGenerico.ACTIVO, description="Estado del proveedor: ACTIVO o INACTIVO")


class JProveedorCreate(JProveedorBase):
    pass


class JProveedorUpdate(BaseModel):
    nit: Optional[str] = Field(None, min_length=3, max_length=20)
    razon_social: Optional[str] = Field(None, min_length=2, max_length=120)
    telefono: Optional[str] = Field(None, max_length=30)
    correo: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=150)
    estado: Optional[JEstadoGenerico] = None


class JProveedorResponse(BaseModel):
    id: str
    nit: str
    razon_social: str
    telefono: Optional[str] = ""
    correo: Optional[str] = None
    direccion: Optional[str] = ""
    estado: str

    model_config = ConfigDict(from_attributes=True)
