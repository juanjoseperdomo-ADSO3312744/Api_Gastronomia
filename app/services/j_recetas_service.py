from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from app.repositories.j_recetas_repository import j_recetas_repo
from app.repositories.j_productos_repository import j_productos_repo
from app.repositories.j_insumos_repository import j_insumos_repo
from app.schemas.j_recetas_schema import JRecetaCreate, JRecetaUpdate, JRecetaProductoDetalleResponse, JRecetaResponse


class JRecetasService:
    def _j_enriquecer_item_receta(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Añade los nombres y costos del producto y del insumo."""
        if item:
            prod = j_productos_repo.j_obtener_por_id(str(item.get("id_producto")))
            ins = j_insumos_repo.j_obtener_por_id(str(item.get("id_insumo")))
            item["producto_nombre"] = prod["nombre"] if prod else "Desconocido"
            item["insumo_nombre"] = ins["nombre"] if ins else "Desconocido"
            item["insumo_unidad_medida"] = ins.get("unidad_medida", "unidad") if ins else "unidad"
            costo_u = float(ins.get("costo_unitario", 0.0)) if ins else 0.0
            item["costo_unitario_insumo"] = costo_u
            item["subtotal_costo"] = round(float(item.get("cantidad", 0.0)) * costo_u, 2)
        return item

    def j_crear_item_receta(self, datos: JRecetaCreate) -> Dict[str, Any]:
        # Validar existencia de producto e insumo
        prod = j_productos_repo.j_obtener_por_id(datos.id_producto)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID '{datos.id_producto}' no existe."
            )
        ins = j_insumos_repo.j_obtener_por_id(datos.id_insumo)
        if not ins:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Insumo con ID '{datos.id_insumo}' no existe."
            )

        # Verificar si ya existe este insumo en la receta del producto
        existentes = j_recetas_repo.j_obtener_por_producto(datos.id_producto)
        for ex in existentes:
            if ex.get("id_insumo") == datos.id_insumo:
                # Actualizar cantidad sumándola o sobreescribiéndola
                nuevo_total = float(ex["cantidad"]) + float(datos.cantidad)
                act = j_recetas_repo.j_actualizar(ex["id"], {"cantidad": nuevo_total})
                return self._j_enriquecer_item_receta(act)

        doc = datos.model_dump()
        doc["id_producto"] = str(datos.id_producto)
        doc["id_insumo"] = str(datos.id_insumo)
        doc["cantidad"] = float(datos.cantidad)
        creado = j_recetas_repo.j_crear(doc)
        return self._j_enriquecer_item_receta(creado)

    def j_obtener_por_id(self, id_receta: str) -> Dict[str, Any]:
        item = j_recetas_repo.j_obtener_por_id(id_receta)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ítem de receta con ID '{id_receta}' no encontrado."
            )
        return self._j_enriquecer_item_receta(item)

    def j_listar_recetas(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        items = j_recetas_repo.j_obtener_todos(salto=salto, limite=limite)
        return [self._j_enriquecer_item_receta(it) for it in items]

    def j_obtener_receta_producto(self, id_producto: str) -> JRecetaProductoDetalleResponse:
        """
        Retorna los insumos y cantidades de la receta de un producto (RF05).
        """
        prod = j_productos_repo.j_obtener_por_id(id_producto)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID '{id_producto}' no existe."
            )
        items = j_recetas_repo.j_obtener_por_producto(id_producto)
        items_enriquecidos = [self._j_enriquecer_item_receta(it) for it in items]
        costo_total = sum(float(it.get("subtotal_costo", 0.0)) for it in items_enriquecidos)

        return JRecetaProductoDetalleResponse(
            id_producto=prod["id"],
            nombre_producto=prod["nombre"],
            precio_venta=float(prod.get("precio_venta", 0.0)),
            items_receta=[JRecetaResponse(**it) for it in items_enriquecidos],
            costo_total_receta=round(costo_total, 2)
        )

    def j_actualizar_item_receta(self, id_receta: str, datos: JRecetaUpdate) -> Dict[str, Any]:
        item_existente = j_recetas_repo.j_obtener_por_id(id_receta)
        if not item_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ítem de receta con ID '{id_receta}' no encontrado."
            )
        datos_act = datos.model_dump(exclude_unset=True)
        if "id_producto" in datos_act and datos_act["id_producto"]:
            if not j_productos_repo.j_obtener_por_id(datos_act["id_producto"]):
                raise HTTPException(status_code=404, detail="Producto no existe.")
        if "id_insumo" in datos_act and datos_act["id_insumo"]:
            if not j_insumos_repo.j_obtener_por_id(datos_act["id_insumo"]):
                raise HTTPException(status_code=404, detail="Insumo no existe.")

        act = j_recetas_repo.j_actualizar(id_receta, datos_act)
        return self._j_enriquecer_item_receta(act)

    def j_eliminar_item_receta(self, id_receta: str) -> Dict[str, Any]:
        item = j_recetas_repo.j_obtener_por_id(id_receta)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ítem de receta con ID '{id_receta}' no encontrado."
            )
        j_recetas_repo.j_eliminar_fisico(id_receta)
        return {"mensaje": "Ítem de receta eliminado con éxito.", "id": id_receta}


j_recetas_service = JRecetasService()
