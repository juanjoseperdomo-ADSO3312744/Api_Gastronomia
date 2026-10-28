from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from app.repositories.j_base_repository import JBaseRepository
from app.database.j_conexion_mongo import j_validar_objectid, j_serializar_lista, j_serializar_doc


class JInsumosRepository(JBaseRepository):
    def __init__(self):
        super().__init__("insumos")

    def j_buscar_por_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        return self.j_buscar_uno({"nombre": {"$regex": f"^{nombre.strip()}$", "$options": "i"}})

    def j_obtener_stock_bajo(self) -> List[Dict[str, Any]]:
        """
        Retorna insumos cuyo stock_actual sea menor o igual al stock_minimo (RF07).
        """
        filtro = {
            "$expr": {"$lte": ["$stock_actual", "$stock_minimo"]},
            "estado": "ACTIVO"
        }
        cursor = self.coleccion.find(filtro).sort("stock_actual", 1)
        return j_serializar_lista(list(cursor))

    def j_obtener_por_vencer(self, dias: int = 7) -> List[Dict[str, Any]]:
        """
        Retorna insumos cuya fecha_vencimiento se encuentre en los próximos N días (RF07).
        """
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        limite_str = (datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")

        filtro = {
            "fecha_vencimiento": {"$gte": hoy_str, "$lte": limite_str},
            "estado": "ACTIVO"
        }
        cursor = self.coleccion.find(filtro).sort("fecha_vencimiento", 1)
        return j_serializar_lista(list(cursor))

    def j_incrementar_stock_y_costo(self, id_insumo: str, cantidad: float, nuevo_costo: float) -> Optional[Dict[str, Any]]:
        """
        Regla RN02: Al registrar una compra se incrementa stock_actual y actualiza costo_unitario.
        """
        obj_id = j_validar_objectid(id_insumo)
        self.coleccion.update_one(
            {"_id": obj_id},
            {
                "$inc": {"stock_actual": float(cantidad)},
                "$set": {"costo_unitario": float(nuevo_costo)}
            }
        )
        return self.j_obtener_por_id(id_insumo)

    def j_descontar_stock(self, id_insumo: str, cantidad: float) -> Optional[Dict[str, Any]]:
        """
        Regla RN03: Descuenta la cantidad consumida del insumo al entregar el pedido.
        """
        obj_id = j_validar_objectid(id_insumo)
        self.coleccion.update_one(
            {"_id": obj_id},
            {"$inc": {"stock_actual": -float(cantidad)}}
        )
        return self.j_obtener_por_id(id_insumo)


j_insumos_repo = JInsumosRepository()
