from typing import Optional, List, Dict, Any
from app.repositories.j_pedidos_repository import j_pedidos_repo
from app.repositories.j_productos_repository import j_productos_repo
from app.repositories.j_categorias_repository import j_categorias_repo
from app.repositories.j_clientes_repository import j_clientes_repo
from app.schemas.j_reportes_schema import (
    JReporteVentasResponse,
    JReporteVentasDetallePedido,
    JReporteProductosMasVendidosResponse,
    JRankingProductoItem
)


class JReportesService:
    def j_reporte_ventas(self, desde: Optional[str] = None, hasta: Optional[str] = None) -> JReporteVentasResponse:
        """
        Genera el reporte de total vendido y número de pedidos en un rango de fechas (RF11).
        """
        resultado = j_pedidos_repo.j_reporte_ventas(desde=desde, hasta=hasta)
        pedidos_detalle: List[JReporteVentasDetallePedido] = []

        for p in resultado["pedidos"]:
            cli = j_clientes_repo.j_obtener_por_id(str(p.get("id_cliente")))
            cli_nombre = f"{cli.get('nombres', '')} {cli.get('apellidos', '')}".strip() if cli else "Desconocido"

            pedidos_detalle.append(
                JReporteVentasDetallePedido(
                    id_pedido=p["id"],
                    fecha_pedido=p.get("fecha_pedido", ""),
                    cliente_nombre=cli_nombre,
                    tipo_pedido=p.get("tipo_pedido", "MESA"),
                    estado=p.get("estado", "PENDIENTE"),
                    total=float(p.get("total", 0.0))
                )
            )

        return JReporteVentasResponse(
            fecha_desde=resultado["fecha_desde"],
            fecha_hasta=resultado["fecha_hasta"],
            total_vendido=resultado["total_vendido"],
            numero_pedidos=resultado["numero_pedidos"],
            ticket_promedio=resultado["ticket_promedio"],
            pedidos=pedidos_detalle
        )

    def j_productos_mas_vendidos(self, limite: int = 10) -> JReporteProductosMasVendidosResponse:
        """
        Genera el ranking de productos más vendidos en la unidad productiva (RF11).
        """
        ranking_raw = j_pedidos_repo.j_ranking_productos_mas_vendidos(limite=limite)
        ranking_items: List[JRankingProductoItem] = []

        for r in ranking_raw:
            prod = j_productos_repo.j_obtener_por_id(r["id_producto"])
            cat_nombre = None
            if prod:
                cat = j_categorias_repo.j_obtener_por_id(str(prod.get("id_categoria", "")))
                cat_nombre = cat.get("nombre") if cat else None

            ranking_items.append(
                JRankingProductoItem(
                    id_producto=r["id_producto"],
                    codigo=prod.get("codigo") if prod else None,
                    nombre=prod.get("nombre", "Producto Desconocido") if prod else "Producto Desconocido",
                    categoria_nombre=cat_nombre,
                    total_unidades_vendidas=r["total_unidades_vendidas"],
                    total_recaudado=r["total_recaudado"],
                    numero_pedidos=r["numero_pedidos"]
                )
            )

        return JReporteProductosMasVendidosResponse(
            limite=limite,
            total_productos_en_ranking=len(ranking_items),
            ranking=ranking_items
        )


j_reportes_service = JReportesService()
