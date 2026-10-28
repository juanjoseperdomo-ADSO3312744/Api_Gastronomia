from typing import List, Dict, Any, Optional
from app.repositories.j_base_repository import JBaseRepository
from app.database.j_conexion_mongo import j_validar_objectid, j_serializar_lista, j_serializar_doc


class JPedidosRepository(JBaseRepository):
    def __init__(self):
        super().__init__("pedidos")

    def j_obtener_por_cliente(self, id_cliente: str) -> List[Dict[str, Any]]:
        cursor = self.coleccion.find({"id_cliente": str(id_cliente)}).sort("fecha_pedido", -1)
        return j_serializar_lista(list(cursor))

    def j_obtener_por_estado(self, estado: str) -> List[Dict[str, Any]]:
        cursor = self.coleccion.find({"estado": estado.upper()}).sort("fecha_pedido", -1)
        return j_serializar_lista(list(cursor))

    def j_actualizar_estado(self, id_pedido: str, nuevo_estado: str) -> Optional[Dict[str, Any]]:
        return self.j_actualizar(id_pedido, {"estado": nuevo_estado})

    def j_tiene_pedidos_de_cliente(self, id_cliente: str) -> bool:
        doc = self.coleccion.find_one({"id_cliente": str(id_cliente)})
        return doc is not None

    def j_tiene_pedidos_con_producto(self, id_producto: str) -> bool:
        doc = self.coleccion.find_one({"detalle.id_producto": str(id_producto)})
        return doc is not None

    def j_tiene_pedidos_de_usuario(self, id_usuario: str) -> bool:
        doc = self.coleccion.find_one({"id_usuario": str(id_usuario)})
        return doc is not None

    def j_reporte_ventas(self, desde: Optional[str] = None, hasta: Optional[str] = None) -> Dict[str, Any]:
        """
        Calcula el total vendido y la cantidad de pedidos en un rango de fechas (RF11).
        Excluye pedidos anulados.
        """
        filtro: Dict[str, Any] = {"estado": {"$ne": "ANULADO"}}

        if desde and hasta:
            filtro["fecha_pedido"] = {"$gte": f"{desde}T00:00:00", "$lte": f"{hasta}T23:59:59"}
        elif desde:
            filtro["fecha_pedido"] = {"$gte": f"{desde}T00:00:00"}
        elif hasta:
            filtro["fecha_pedido"] = {"$lte": f"{hasta}T23:59:59"}

        pedidos = list(self.coleccion.find(filtro).sort("fecha_pedido", -1))
        total_vendido = sum(float(p.get("total", 0.0)) for p in pedidos)
        numero_pedidos = len(pedidos)
        ticket_promedio = round(total_vendido / numero_pedidos, 2) if numero_pedidos > 0 else 0.0

        return {
            "fecha_desde": desde,
            "fecha_hasta": hasta,
            "total_vendido": round(total_vendido, 2),
            "numero_pedidos": numero_pedidos,
            "ticket_promedio": ticket_promedio,
            "pedidos": j_serializar_lista(pedidos)
        }

    def j_ranking_productos_mas_vendidos(self, limite: int = 10) -> List[Dict[str, Any]]:
        """
        Ranking de productos más vendidos utilizando aggregation pipeline de MongoDB (RF11).
        """
        pipeline = [
            {"$match": {"estado": {"$ne": "ANULADO"}}},
            {"$unwind": "$detalle"},
            {
                "$group": {
                    "_id": "$detalle.id_producto",
                    "total_unidades_vendidas": {"$sum": "$detalle.cantidad"},
                    "total_recaudado": {"$sum": "$detalle.subtotal"},
                    "numero_pedidos": {"$sum": 1}
                }
            },
            {"$sort": {"total_unidades_vendidas": -1}},
            {"$limit": limite}
        ]
        resultados = list(self.coleccion.aggregate(pipeline))
        return [
            {
                "id_producto": str(r["_id"]),
                "total_unidades_vendidas": round(float(r["total_unidades_vendidas"]), 2),
                "total_recaudado": round(float(r["total_recaudado"]), 2),
                "numero_pedidos": int(r["numero_pedidos"])
            }
            for r in resultados
        ]


j_pedidos_repo = JPedidosRepository()
