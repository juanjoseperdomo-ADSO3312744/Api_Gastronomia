from typing import List, Dict, Any
from fastapi import HTTPException, status
from app.repositories.j_clientes_repository import j_clientes_repo
from app.repositories.j_pedidos_repository import j_pedidos_repo
from app.schemas.j_clientes_schema import JClienteCreate, JClienteUpdate


class JClientesService:
    def j_crear_cliente(self, datos: JClienteCreate) -> Dict[str, Any]:
        if j_clientes_repo.j_buscar_por_identificacion(datos.identificacion):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un cliente registrado con la identificación '{datos.identificacion}'."
            )
        doc = datos.model_dump()
        doc["identificacion"] = datos.identificacion.strip()
        doc["nombres"] = datos.nombres.strip()
        doc["apellidos"] = datos.apellidos.strip()
        return j_clientes_repo.j_crear(doc)

    def j_obtener_por_id(self, id_cliente: str) -> Dict[str, Any]:
        cliente = j_clientes_repo.j_obtener_por_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID '{id_cliente}' no encontrado."
            )
        return cliente

    def j_listar_clientes(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        return j_clientes_repo.j_obtener_todos(salto=salto, limite=limite, orden=[("apellidos", 1)])

    def j_actualizar_cliente(self, id_cliente: str, datos: JClienteUpdate) -> Dict[str, Any]:
        cliente_existente = j_clientes_repo.j_obtener_por_id(id_cliente)
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID '{id_cliente}' no encontrado."
            )

        datos_act = datos.model_dump(exclude_unset=True)
        if "identificacion" in datos_act and datos_act["identificacion"]:
            nueva_id = datos_act["identificacion"].strip()
            encontrado = j_clientes_repo.j_buscar_por_identificacion(nueva_id)
            if encontrado and encontrado["id"] != id_cliente:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"La identificación '{nueva_id}' ya pertenece a otro cliente."
                )
            datos_act["identificacion"] = nueva_id

        return j_clientes_repo.j_actualizar(id_cliente, datos_act)

    def j_eliminar_cliente(self, id_cliente: str) -> Dict[str, Any]:
        """
        Regla RN04: Si tiene pedidos asociados, se realiza borrado lógico a INACTIVO.
        """
        cliente = j_clientes_repo.j_obtener_por_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID '{id_cliente}' no encontrado."
            )

        tiene_pedidos = j_pedidos_repo.j_tiene_pedidos_de_cliente(id_cliente)
        if tiene_pedidos:
            j_clientes_repo.j_cambiar_estado(id_cliente, "INACTIVO")
            return {
                "mensaje": "El cliente tiene pedidos registrados. Se realizó borrado lógico (estado INACTIVO).",
                "tipo_eliminacion": "LOGICA",
                "id": id_cliente
            }
        else:
            j_clientes_repo.j_eliminar_fisico(id_cliente)
            return {
                "mensaje": "Cliente eliminado físicamente con éxito.",
                "tipo_eliminacion": "FISICA",
                "id": id_cliente
            }

    def j_obtener_pedidos_cliente(self, id_cliente: str) -> List[Dict[str, Any]]:
        self.j_obtener_por_id(id_cliente)  # Valida que exista
        return j_pedidos_repo.j_obtener_por_cliente(id_cliente)


j_clientes_service = JClientesService()
