from typing import List, Dict, Any, Optional
from app.repositories.j_base_repository import JBaseRepository
from app.database.j_conexion_mongo import j_serializar_lista, j_serializar_doc


class JCalificacionesRepository(JBaseRepository):
    def __init__(self):
        super().__init__("calificaciones")

    def j_obtener_por_pedido(self, id_pedido: str) -> Optional[Dict[str, Any]]:
        doc = self.coleccion.find_one({"id_pedido": str(id_pedido)})
        return j_serializar_doc(doc)

    def j_obtener_por_producto(self, id_producto: str) -> List[Dict[str, Any]]:
        cursor = self.coleccion.find({"productos.id_producto": str(id_producto)})
        return j_serializar_lista(list(cursor))


j_calificaciones_repo = JCalificacionesRepository()
