from typing import Optional, List, Dict, Any
from app.repositories.j_base_repository import JBaseRepository
from app.database.j_conexion_mongo import j_validar_objectid, j_serializar_lista


class JProductosRepository(JBaseRepository):
    def __init__(self):
        super().__init__("productos")

    def j_buscar_por_codigo(self, codigo: str) -> Optional[Dict[str, Any]]:
        return self.j_buscar_uno({"codigo": codigo.strip().upper()})

    def j_buscar_por_categoria(self, id_categoria: str) -> List[Dict[str, Any]]:
        # Puede estar guardado como string o como ObjectId
        filtro = {
            "$or": [
                {"id_categoria": id_categoria},
                {"id_categoria": j_validar_objectid(id_categoria) if len(id_categoria) == 24 else None}
            ]
        }
        # Filtrar valores None en $or
        filtro["$or"] = [cond for cond in filtro["$or"] if cond["id_categoria"] is not None]
        return self.j_obtener_todos(filtro=filtro)


j_productos_repo = JProductosRepository()
