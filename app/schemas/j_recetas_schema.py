from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class JRecetaItemBase(BaseModel):
    id_producto: str = Field(..., description="ID del producto")
    id_insumo: str = Field(..., description="ID del insumo utilizado en la receta")
    cantidad: float = Field(..., gt=0, description="Cantidad requerida por unidad de producto")


class JRecetaCreate(JRecetaItemBase):
    pass


class JRecetaUpdate(BaseModel):
    id_producto: Optional[str] = None
    id_insumo: Optional[str] = None
    cantidad: Optional[float] = Field(None, gt=0)


class JRecetaResponse(BaseModel):
    id: str
    id_producto: str
    producto_nombre: Optional[str] = None
    id_insumo: str
    insumo_nombre: Optional[str] = None
    insumo_unidad_medida: Optional[str] = None
    costo_unitario_insumo: Optional[float] = None
    cantidad: float
    subtotal_costo: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class JRecetaProductoDetalleResponse(BaseModel):
    id_producto: str
    nombre_producto: str
    precio_venta: float
    items_receta: List[JRecetaResponse]
    costo_total_receta: float
