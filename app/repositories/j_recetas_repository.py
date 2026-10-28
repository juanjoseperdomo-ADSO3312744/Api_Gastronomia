from typing import List, Dict, Any, Optional
from app.repositories.j_base_repository import JBaseRepository
from app.database.j_conexion_mongo import j_validar_objectid, j_serializar_lista


class JRecetasRepository(JBaseRepository):
    def __init__(self):
        super().__init__("recetas")

    def j_obtener_por_producto(self, id_producto: str) -> List[Dict[str, Any]]:
        cursor = self.coleccion.find({"id_producto": str(id_producto)})
        return j_serializar_lista(list(cursor))

    def j_obtener_por_insumo(self, id_insumo: str) -> List[Dict[str, Any]]:
        cursor = self.coleccion.find({"id_insumo": str(id_insumo)})
        return j_serializar_lista(list(cursor))

    def j_eliminar_por_producto(self, id_producto: str) -> int:
        res = self.coleccion.delete_many({"id_producto": str(id_producto)})
        return res.deleted_count


j_recetas_repo = JRecetasRepository()
