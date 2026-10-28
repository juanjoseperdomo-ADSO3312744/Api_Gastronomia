from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.models.j_models import JEstadoProducto


class JProductoBase(BaseModel):
    codigo: str = Field(..., min_length=2, max_length=20, description="Código interno único del producto")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del producto")
    descripcion: Optional[str] = Field(default="", description="Descripción detallada del producto")
    precio_venta: float = Field(..., gt=0, description="Precio de venta mayor a cero")
    unidad_venta: str = Field(..., min_length=1, max_length=20, description="Porción, unidad, libra, vaso...")
    id_categoria: str = Field(..., description="ID de la categoría a la que pertenece")
    estado: JEstadoProducto = Field(default=JEstadoProducto.DISPONIBLE, description="DISPONIBLE, AGOTADO o INACTIVO")


class JProductoCreate(JProductoBase):
    pass


class JProductoUpdate(BaseModel):
    codigo: Optional[str] = Field(None, min_length=2, max_length=20)
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    precio_venta: Optional[float] = Field(None, gt=0)
    unidad_venta: Optional[str] = Field(None, min_length=1, max_length=20)
    id_categoria: Optional[str] = None
    estado: Optional[JEstadoProducto] = None


class JProductoResponse(BaseModel):
    id: str
    codigo: str
    nombre: str
    descripcion: Optional[str] = ""
    precio_venta: float
    unidad_venta: str
    id_categoria: str
    categoria_nombre: Optional[str] = None
    estado: str

    model_config = ConfigDict(from_attributes=True)


class JInsumoDetalleCosto(BaseModel):
    id_insumo: str
    nombre_insumo: str
    unidad_medida: str
    cantidad_receta: float
    costo_unitario: float
    subtotal_costo: float


class JProductoCostoMargenResponse(BaseModel):
    """
    Respuesta para el endpoint de cálculo de costo de producción y margen comercial (RF06).
    """
    id_producto: str
    codigo: str
    nombre_producto: str
    precio_venta: float
    costo_produccion: float
    margen_ganancia: float
    porcentaje_margen: float
    detalle_insumos: List[JInsumoDetalleCosto]
