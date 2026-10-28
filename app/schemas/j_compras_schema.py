from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class JDetalleCompraItemCreate(BaseModel):
    id_insumo: str = Field(..., description="ID del insumo comprado")
    cantidad: float = Field(..., gt=0, description="Cantidad adquirida")
    costo_unitario: float = Field(..., ge=0, description="Costo unitario de compra")


class JDetalleCompraItemResponse(BaseModel):
    id_insumo: str
    nombre_insumo: Optional[str] = None
    unidad_medida: Optional[str] = None
    cantidad: float
    costo_unitario: float
    subtotal: float


class JCompraCreate(BaseModel):
    numero_factura: str = Field(..., min_length=1, max_length=30, description="Número de factura del proveedor")
    fecha_compra: Optional[str] = Field(default=None, description="Fecha de la compra en formato ISO o YYYY-MM-DD (por defecto actual)")
    id_proveedor: str = Field(..., description="ID del proveedor asociado")
    detalle: List[JDetalleCompraItemCreate] = Field(..., min_length=1, description="Lista de insumos adquiridos en la compra")


class JCompraUpdate(BaseModel):
    numero_factura: Optional[str] = Field(None, min_length=1, max_length=30)
    fecha_compra: Optional[str] = None
    id_proveedor: Optional[str] = None


class JCompraResponse(BaseModel):
    id: str
    numero_factura: str
    fecha_compra: str
    id_proveedor: str
    proveedor_razon_social: Optional[str] = None
    id_usuario: str
    usuario_nombre: Optional[str] = None
    total: float
    detalle: List[JDetalleCompraItemResponse]

    model_config = ConfigDict(from_attributes=True)
