from typing import List, Dict, Any, Optional
from app.repositories.j_base_repository import JBaseRepository
from app.database.j_conexion_mongo import j_serializar_lista


class JComprasRepository(JBaseRepository):
    def __init__(self):
        super().__init__("compras")

    def j_buscar_por_numero_factura(self, numero_factura: str) -> Optional[Dict[str, Any]]:
        return self.j_buscar_uno({"numero_factura": numero_factura.strip()})

    def j_obtener_por_proveedor(self, id_proveedor: str) -> List[Dict[str, Any]]:
        cursor = self.coleccion.find({"id_proveedor": str(id_proveedor)}).sort("fecha_compra", -1)
        return j_serializar_lista(list(cursor))

    def j_tiene_compras_con_insumo(self, id_insumo: str) -> bool:
        doc = self.coleccion.find_one({"detalle.id_insumo": str(id_insumo)})
        return doc is not None

    def j_tiene_compras_de_proveedor(self, id_proveedor: str) -> bool:
        doc = self.coleccion.find_one({"id_proveedor": str(id_proveedor)})
        return doc is not None

    def j_tiene_compras_de_usuario(self, id_usuario: str) -> bool:
        doc = self.coleccion.find_one({"id_usuario": str(id_usuario)})
        return doc is not None


j_compras_repo = JComprasRepository()
