from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.j_models import JTipoPedido, JEstadoPedido


class JDetallePedidoItemCreate(BaseModel):
    id_producto: str = Field(..., description="ID del producto a ordenar")
    cantidad: float = Field(..., gt=0, description="Cantidad del producto")


class JDetallePedidoItemResponse(BaseModel):
    id_producto: str
    nombre_producto: Optional[str] = None
    cantidad: float
    precio_unitario: float
    subtotal: float


class JPedidoCreate(BaseModel):
    id_cliente: str = Field(..., description="ID del cliente que realiza el pedido")
    tipo_pedido: JTipoPedido = Field(..., description="MESA, PARA_LLEVAR o EVENTO")
    detalle: List[JDetallePedidoItemCreate] = Field(..., min_length=1, description="Lista de productos del pedido")
    observaciones: Optional[str] = Field(default="", description="Observaciones especiales")


class JPedidoUpdate(BaseModel):
    id_cliente: Optional[str] = None
    tipo_pedido: Optional[JTipoPedido] = None
    detalle: Optional[List[JDetallePedidoItemCreate]] = None
    observaciones: Optional[str] = None


class JPedidoEstadoUpdate(BaseModel):
    """
    Esquema para cambio de estado de pedido (PATCH /pedidos/{id}/estado).
    Aplica las reglas de negocio RN03 y RN05.
    """
    estado: JEstadoPedido = Field(..., description="Nuevo estado: PENDIENTE, EN_PREPARACION, ENTREGADO o ANULADO")


class JPedidoResponse(BaseModel):
    id: str
    fecha_pedido: str
    id_cliente: str
    cliente_nombre: Optional[str] = None
    id_usuario: str
    usuario_nombre: Optional[str] = None
    tipo_pedido: str
    estado: str
    total: float
    detalle: List[JDetallePedidoItemResponse]
    observaciones: Optional[str] = ""

    model_config = ConfigDict(from_attributes=True)
