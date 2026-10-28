from typing import List, Dict, Any
from fastapi import HTTPException, status
from app.repositories.j_insumos_repository import j_insumos_repo
from app.repositories.j_recetas_repository import j_recetas_repo
from app.repositories.j_compras_repository import j_compras_repo
from app.schemas.j_insumos_schema import JInsumoCreate, JInsumoUpdate


class JInsumosService:
    def j_crear_insumo(self, datos: JInsumoCreate) -> Dict[str, Any]:
        if j_insumos_repo.j_buscar_por_nombre(datos.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un insumo registrado con el nombre '{datos.nombre}'."
            )
        doc = datos.model_dump()
        doc["nombre"] = datos.nombre.strip()
        return j_insumos_repo.j_crear(doc)

    def j_obtener_por_id(self, id_insumo: str) -> Dict[str, Any]:
        insumo = j_insumos_repo.j_obtener_por_id(id_insumo)
        if not insumo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Insumo con ID '{id_insumo}' no encontrado."
            )
        return insumo

    def j_listar_insumos(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        return j_insumos_repo.j_obtener_todos(salto=salto, limite=limite, orden=[("nombre", 1)])

    def j_actualizar_insumo(self, id_insumo: str, datos: JInsumoUpdate) -> Dict[str, Any]:
        insumo_existente = j_insumos_repo.j_obtener_por_id(id_insumo)
        if not insumo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Insumo con ID '{id_insumo}' no encontrado."
            )

        datos_act = datos.model_dump(exclude_unset=True)
        if "nombre" in datos_act and datos_act["nombre"]:
            nuevo_nom = datos_act["nombre"].strip()
            encontrado = j_insumos_repo.j_buscar_por_nombre(nuevo_nom)
            if encontrado and encontrado["id"] != id_insumo:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El nombre '{nuevo_nom}' ya pertenece a otro insumo."
                )
            datos_act["nombre"] = nuevo_nom

        return j_insumos_repo.j_actualizar(id_insumo, datos_act)

    def j_eliminar_insumo(self, id_insumo: str) -> Dict[str, Any]:
        """
        Regla RN04: Si tiene movimientos (usado en recetas o en compras registradas),
        se realiza borrado lógico cambiando su estado a INACTIVO.
        """
        insumo = j_insumos_repo.j_obtener_por_id(id_insumo)
        if not insumo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Insumo con ID '{id_insumo}' no encontrado."
            )

        en_recetas = len(j_recetas_repo.j_obtener_por_insumo(id_insumo)) > 0
        en_compras = j_compras_repo.j_tiene_compras_con_insumo(id_insumo)

        if en_recetas or en_compras:
            j_insumos_repo.j_cambiar_estado(id_insumo, "INACTIVO")
            return {
                "mensaje": "El insumo tiene movimientos asociados (recetas o compras). Se realizó borrado lógico (estado INACTIVO).",
                "tipo_eliminacion": "LOGICA",
                "id": id_insumo
            }
        else:
            j_insumos_repo.j_eliminar_fisico(id_insumo)
            return {
                "mensaje": "Insumo eliminado físicamente con éxito.",
                "tipo_eliminacion": "FISICA",
                "id": id_insumo
            }

    def j_obtener_stock_bajo(self) -> List[Dict[str, Any]]:
        return j_insumos_repo.j_obtener_stock_bajo()

    def j_obtener_por_vencer(self, dias: int = 7) -> List[Dict[str, Any]]:
        return j_insumos_repo.j_obtener_por_vencer(dias=dias)


j_insumos_service = JInsumosService()
