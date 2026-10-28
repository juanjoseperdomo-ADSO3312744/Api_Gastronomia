from typing import Optional, List
from pydantic import BaseModel, Field


class JReporteVentasDetallePedido(BaseModel):
    id_pedido: str
    fecha_pedido: str
    cliente_nombre: Optional[str] = None
    tipo_pedido: str
    estado: str
    total: float


class JReporteVentasResponse(BaseModel):
    fecha_desde: Optional[str] = None
    fecha_hasta: Optional[str] = None
    total_vendido: float = Field(..., description="Monto total acumulado de ventas")
    numero_pedidos: int = Field(..., description="Cantidad total de pedidos registrados en el periodo")
    ticket_promedio: float = Field(..., description="Promedio de venta por pedido")
    pedidos: List[JReporteVentasDetallePedido] = Field(default=[], description="Listado de pedidos incluidos")


class JRankingProductoItem(BaseModel):
    id_producto: str
    codigo: Optional[str] = None
    nombre: str
    categoria_nombre: Optional[str] = None
    total_unidades_vendidas: float = Field(..., description="Suma total de cantidades vendidas")
    total_recaudado: float = Field(..., description="Total en dinero generado por el producto")
    numero_pedidos: int = Field(..., description="En cuántos pedidos fue ordenado")


class JReporteProductosMasVendidosResponse(BaseModel):
    limite: int
    total_productos_en_ranking: int
    ranking: List[JRankingProductoItem]
