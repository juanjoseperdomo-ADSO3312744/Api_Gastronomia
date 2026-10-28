from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.j_models import JUnidadMedida, JEstadoGenerico


class JInsumoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre único del insumo")
    unidad_medida: JUnidadMedida = Field(..., description="Unidad de medida: g, kg, ml, l, lb, unidad")
    stock_actual: float = Field(default=0.0, ge=0, description="Existencias actuales en inventario")
    stock_minimo: float = Field(default=0.0, ge=0, description="Nivel mínimo de alerta de inventario")
    costo_unitario: float = Field(default=0.0, ge=0, description="Costo por unidad de medida")
    fecha_vencimiento: Optional[str] = Field(default=None, description="Fecha de vencimiento en formato YYYY-MM-DD")
    estado: JEstadoGenerico = Field(default=JEstadoGenerico.ACTIVO, description="Estado del insumo: ACTIVO o INACTIVO")


class JInsumoCreate(JInsumoBase):
    pass


class JInsumoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    unidad_medida: Optional[JUnidadMedida] = None
    stock_actual: Optional[float] = Field(None, ge=0)
    stock_minimo: Optional[float] = Field(None, ge=0)
    costo_unitario: Optional[float] = Field(None, ge=0)
    fecha_vencimiento: Optional[str] = None
    estado: Optional[JEstadoGenerico] = None


class JInsumoResponse(BaseModel):
    id: str
    nombre: str
    unidad_medida: str
    stock_actual: float
    stock_minimo: float
    costo_unitario: float
    fecha_vencimiento: Optional[str] = None
    estado: str

    model_config = ConfigDict(from_attributes=True)
