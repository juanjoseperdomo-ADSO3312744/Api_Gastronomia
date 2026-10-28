from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class JProductoCalificacionItem(BaseModel):
    id_producto: str = Field(..., description="ID del producto calificado")
    nombre: Optional[str] = Field(default="", description="Nombre del producto")
    calificacion: int = Field(..., ge=1, le=5, description="Calificación de 1 a 5 estrellas")


class JCalificacionCreate(BaseModel):
    id_pedido: str = Field(..., description="ID del pedido calificado")
    id_cliente: str = Field(..., description="ID del cliente que califica")
    fecha: Optional[str] = Field(default=None, description="Fecha de la calificación en formato ISO (por defecto actual)")
    calificacion_servicio: int = Field(..., ge=1, le=5, description="Calificación global del servicio (1 a 5)")
    comentario: Optional[str] = Field(default="", description="Opinión o comentario sobre el servicio y comida")
    productos: List[JProductoCalificacionItem] = Field(default=[], description="Calificación detallada por producto")


class JCalificacionResponse(BaseModel):
    id: str
    id_pedido: str
    id_cliente: str
    cliente_nombre: Optional[str] = None
    fecha: str
    calificacion_servicio: int
    comentario: Optional[str] = ""
    productos: List[JProductoCalificacionItem]

    model_config = ConfigDict(from_attributes=True)


class JCalificacionProductoDetalle(BaseModel):
    id_calificacion: str
    id_pedido: str
    id_cliente: str
    cliente_nombre: Optional[str] = None
    fecha: str
    calificacion: int
    comentario: Optional[str] = ""


class JCalificacionProductoResumen(BaseModel):
    id_producto: str
    nombre_producto: str
    promedio_calificacion: float
    total_calificaciones: int
    calificaciones: List[JCalificacionProductoDetalle]
