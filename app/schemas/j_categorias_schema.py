from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.j_models import JEstadoGenerico


class JCategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=60, description="Nombre único de la categoría")
    descripcion: Optional[str] = Field(default="", max_length=200, description="Descripción de la categoría")
    estado: JEstadoGenerico = Field(default=JEstadoGenerico.ACTIVO, description="Estado de la categoría")


class JCategoriaCreate(JCategoriaBase):
    pass


class JCategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=60)
    descripcion: Optional[str] = Field(None, max_length=200)
    estado: Optional[JEstadoGenerico] = None


class JCategoriaResponse(BaseModel):
    id: str
    nombre: str
    descripcion: Optional[str] = ""
    estado: str

    model_config = ConfigDict(from_attributes=True)
