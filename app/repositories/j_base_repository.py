from typing import Optional, List, Dict, Any
from bson import ObjectId
from pymongo.collection import Collection
from app.database.j_conexion_mongo import (
    j_obtener_bd,
    j_validar_objectid,
    j_serializar_doc,
    j_serializar_lista,
)


class JBaseRepository:
    """
    Repositorio base genérico con operaciones CRUD para MongoDB utilizando PyMongo.
    """
    def __init__(self, nombre_coleccion: str):
        self.nombre_coleccion = nombre_coleccion

    @property
    def coleccion(self) -> Collection:
        return j_obtener_bd()[self.nombre_coleccion]

    def j_crear(self, documento: Dict[str, Any]) -> Dict[str, Any]:
        doc_insertar = documento.copy()
        resultado = self.coleccion.insert_one(doc_insertar)
        doc_creado = self.coleccion.find_one({"_id": resultado.inserted_id})
        return j_serializar_doc(doc_creado)

    def j_obtener_por_id(self, id_str: str) -> Optional[Dict[str, Any]]:
        obj_id = j_validar_objectid(id_str)
        doc = self.coleccion.find_one({"_id": obj_id})
        return j_serializar_doc(doc)

    def j_buscar_uno(self, filtro: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        doc = self.coleccion.find_one(filtro)
        return j_serializar_doc(doc)

    def j_obtener_todos(
        self,
        filtro: Optional[Dict[str, Any]] = None,
        salto: int = 0,
        limite: int = 100,
        orden: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        criterio = filtro or {}
        cursor = self.coleccion.find(criterio)
        if orden:
            cursor = cursor.sort(orden)
        cursor = cursor.skip(salto).limit(limite)
        return j_serializar_lista(list(cursor))

    def j_actualizar(self, id_str: str, datos_actualizar: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        obj_id = j_validar_objectid(id_str)
        # Limpiar claves None si se desea o conservar
        datos_limpios = {k: v for k, v in datos_actualizar.items() if v is not None and k != "id" and k != "_id"}
        if not datos_limpios:
            return self.j_obtener_por_id(id_str)

        self.coleccion.update_one({"_id": obj_id}, {"$set": datos_limpios})
        doc_actualizado = self.coleccion.find_one({"_id": obj_id})
        return j_serializar_doc(doc_actualizado)

    def j_eliminar_fisico(self, id_str: str) -> bool:
        obj_id = j_validar_objectid(id_str)
        resultado = self.coleccion.delete_one({"_id": obj_id})
        return resultado.deleted_count > 0

    def j_cambiar_estado(self, id_str: str, nuevo_estado: str = "INACTIVO") -> Optional[Dict[str, Any]]:
        """
        Borrado lógico cambiando el estado a INACTIVO (Regla RN04).
        """
        return self.j_actualizar(id_str, {"estado": nuevo_estado})

    def j_contar(self, filtro: Optional[Dict[str, Any]] = None) -> int:
        return self.coleccion.count_documents(filtro or {})
