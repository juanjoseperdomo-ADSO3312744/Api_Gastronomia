from typing import List, Dict, Any
from fastapi import HTTPException, status
from app.repositories.j_proveedores_repository import j_proveedores_repo
from app.repositories.j_compras_repository import j_compras_repo
from app.schemas.j_proveedores_schema import JProveedorCreate, JProveedorUpdate


class JProveedoresService:
    def j_crear_proveedor(self, datos: JProveedorCreate) -> Dict[str, Any]:
        if j_proveedores_repo.j_buscar_por_nit(datos.nit):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un proveedor registrado con el NIT '{datos.nit}'."
            )
        doc = datos.model_dump()
        doc["nit"] = datos.nit.strip()
        doc["razon_social"] = datos.razon_social.strip()
        return j_proveedores_repo.j_crear(doc)

    def j_obtener_por_id(self, id_proveedor: str) -> Dict[str, Any]:
        prov = j_proveedores_repo.j_obtener_por_id(id_proveedor)
        if not prov:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID '{id_proveedor}' no encontrado."
            )
        return prov

    def j_listar_proveedores(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        return j_proveedores_repo.j_obtener_todos(salto=salto, limite=limite, orden=[("razon_social", 1)])

    def j_actualizar_proveedor(self, id_proveedor: str, datos: JProveedorUpdate) -> Dict[str, Any]:
        prov_existente = j_proveedores_repo.j_obtener_por_id(id_proveedor)
        if not prov_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID '{id_proveedor}' no encontrado."
            )

        datos_act = datos.model_dump(exclude_unset=True)
        if "nit" in datos_act and datos_act["nit"]:
            nuevo_nit = datos_act["nit"].strip()
            encontrado = j_proveedores_repo.j_buscar_por_nit(nuevo_nit)
            if encontrado and encontrado["id"] != id_proveedor:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El NIT '{nuevo_nit}' ya está registrado con otro proveedor."
                )
            datos_act["nit"] = nuevo_nit

        return j_proveedores_repo.j_actualizar(id_proveedor, datos_act)

    def j_eliminar_proveedor(self, id_proveedor: str) -> Dict[str, Any]:
        """
        Regla RN04: Si el proveedor tiene compras asociadas, se realiza borrado lógico a INACTIVO.
        """
        prov = j_proveedores_repo.j_obtener_por_id(id_proveedor)
        if not prov:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID '{id_proveedor}' no encontrado."
            )

        tiene_compras = j_compras_repo.j_tiene_compras_de_proveedor(id_proveedor)
        if tiene_compras:
            j_proveedores_repo.j_cambiar_estado(id_proveedor, "INACTIVO")
            return {
                "mensaje": "El proveedor tiene compras asociadas. Se realizó borrado lógico (estado INACTIVO).",
                "tipo_eliminacion": "LOGICA",
                "id": id_proveedor
            }
        else:
            j_proveedores_repo.j_eliminar_fisico(id_proveedor)
            return {
                "mensaje": "Proveedor eliminado físicamente con éxito.",
                "tipo_eliminacion": "FISICA",
                "id": id_proveedor
            }

    def j_obtener_compras_proveedor(self, id_proveedor: str) -> List[Dict[str, Any]]:
        self.j_obtener_por_id(id_proveedor)  # Valida que exista
        return j_compras_repo.j_obtener_por_proveedor(id_proveedor)


j_proveedores_service = JProveedoresService()
