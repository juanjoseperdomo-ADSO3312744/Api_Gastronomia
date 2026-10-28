from typing import Optional, Any
from bson import ObjectId
from pymongo import MongoClient
from pymongo.database import Database
from fastapi import HTTPException, status
from app.core.j_config import j_settings


class JMongoConnection:
    """
    Gestor singleton de la conexión a la base de datos MongoDB usando PyMongo.
    """
    _cliente: Optional[MongoClient] = None

    @classmethod
    def j_conectar(cls) -> MongoClient:
        if cls._cliente is None:
            cls._cliente = MongoClient(
                j_settings.MONGO_URI,
                serverSelectionTimeoutMS=5000,
                uuidRepresentation="standard"
            )
        return cls._cliente

    @classmethod
    def j_obtener_base_datos(cls) -> Database:
        cliente = cls.j_conectar()
        return cliente[j_settings.MONGO_DB_NAME]

    @classmethod
    def j_cerrar(cls):
        if cls._cliente is not None:
            cls._cliente.close()
            cls._cliente = None


def j_obtener_bd() -> Database:
    """
    Función de utilidad para obtener la base de datos actual.
    """
    return JMongoConnection.j_obtener_base_datos()


def j_validar_objectid(id_str: str) -> ObjectId:
    """
    Valida y convierte un identificador hexadecimal de 24 caracteres en ObjectId de MongoDB.
    Lanza HTTP 400 si el identificador no tiene formato válido.
    """
    if not id_str or not ObjectId.is_valid(id_str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Identificador inválido: '{id_str}'. Debe ser un ObjectId válido de MongoDB (24 caracteres hexadecimales)."
        )
    return ObjectId(id_str)


def j_serializar_doc(doc: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
    """
    Convierte los campos ObjectId y datetimes a tipos nativos serializables JSON,
    renombrando '_id' a 'id'.
    """
    if doc is None:
        return None

    resultado = {}
    for clave, valor in doc.items():
        if clave == "_id":
            resultado["id"] = str(valor)
        elif isinstance(valor, ObjectId):
            resultado[clave] = str(valor)
        elif isinstance(valor, list):
            resultado[clave] = [
                j_serializar_doc(item) if isinstance(item, dict) else (str(item) if isinstance(item, ObjectId) else item)
                for item in valor
            ]
        elif isinstance(valor, dict):
            resultado[clave] = j_serializar_doc(valor)
        else:
            resultado[clave] = valor
    return resultado


def j_serializar_lista(docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Serializa una lista de documentos de MongoDB.
    """
    return [j_serializar_doc(d) for d in docs if d is not None]
