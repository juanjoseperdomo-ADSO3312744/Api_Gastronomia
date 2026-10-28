from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from app.repositories.j_productos_repository import j_productos_repo
from app.repositories.j_categorias_repository import j_categorias_repo
from app.repositories.j_recetas_repository import j_recetas_repo
from app.repositories.j_insumos_repository import j_insumos_repo
from app.repositories.j_pedidos_repository import j_pedidos_repo
from app.schemas.j_productos_schema import (
    JProductoCreate,
    JProductoUpdate,
    JProductoCostoMargenResponse,
    JInsumoDetalleCosto
)


class JProductosService:
    def _j_enriquecer_producto(self, prod: Dict[str, Any]) -> Dict[str, Any]:
        """Añade el nombre de la categoría al documento del producto."""
        if prod and "id_categoria" in prod:
            cat = j_categorias_repo.j_obtener_por_id(str(prod["id_categoria"]))
            prod["categoria_nombre"] = cat["nombre"] if cat else "Sin categoría"
        return prod

    def j_crear_producto(self, datos: JProductoCreate) -> Dict[str, Any]:
        # Validar categoría
        cat = j_categorias_repo.j_obtener_por_id(datos.id_categoria)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La categoría con ID '{datos.id_categoria}' no existe."
            )

        # Validar código único
        if j_productos_repo.j_buscar_por_codigo(datos.codigo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un producto con el código '{datos.codigo}'."
            )

        doc = datos.model_dump()
        doc["codigo"] = datos.codigo.strip().upper()
        doc["id_categoria"] = str(datos.id_categoria)
        creado = j_productos_repo.j_crear(doc)
        return self._j_enriquecer_producto(creado)

    def j_obtener_por_id(self, id_producto: str) -> Dict[str, Any]:
        prod = j_productos_repo.j_obtener_por_id(id_producto)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID '{id_producto}' no encontrado."
            )
        return self._j_enriquecer_producto(prod)

    def j_listar_productos(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        productos = j_productos_repo.j_obtener_todos(salto=salto, limite=limite, orden=[("nombre", 1)])
        return [self._j_enriquecer_producto(p) for p in productos]

    def j_obtener_por_categoria(self, id_categoria: str) -> List[Dict[str, Any]]:
        # Verificar categoría existente
        cat = j_categorias_repo.j_obtener_por_id(id_categoria)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con ID '{id_categoria}' no encontrada."
            )
        productos = j_productos_repo.j_buscar_por_categoria(id_categoria)
        return [self._j_enriquecer_producto(p) for p in productos]

    def j_actualizar_producto(self, id_producto: str, datos: JProductoUpdate) -> Dict[str, Any]:
        prod_existente = j_productos_repo.j_obtener_por_id(id_producto)
        if not prod_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID '{id_producto}' no encontrado."
            )

        datos_act = datos.model_dump(exclude_unset=True)

        if "codigo" in datos_act and datos_act["codigo"]:
            nuevo_cod = datos_act["codigo"].strip().upper()
            encontrado = j_productos_repo.j_buscar_por_codigo(nuevo_cod)
            if encontrado and encontrado["id"] != id_producto:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El código '{nuevo_cod}' ya pertenece a otro producto."
                )
            datos_act["codigo"] = nuevo_cod

        if "id_categoria" in datos_act and datos_act["id_categoria"]:
            cat = j_categorias_repo.j_obtener_por_id(datos_act["id_categoria"])
            if not cat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"La categoría con ID '{datos_act['id_categoria']}' no existe."
                )
            datos_act["id_categoria"] = str(datos_act["id_categoria"])

        actualizado = j_productos_repo.j_actualizar(id_producto, datos_act)
        return self._j_enriquecer_producto(actualizado)

    def j_eliminar_producto(self, id_producto: str) -> Dict[str, Any]:
        """
        Regla RN04: Si tiene movimientos asociados (recetas asociadas o pedidos registrados),
        se realiza borrado lógico cambiando su estado a INACTIVO.
        """
        prod = j_productos_repo.j_obtener_por_id(id_producto)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID '{id_producto}' no encontrado."
            )

        tiene_recetas = len(j_recetas_repo.j_obtener_por_producto(id_producto)) > 0
        tiene_pedidos = j_pedidos_repo.j_tiene_pedidos_con_producto(id_producto)

        if tiene_recetas or tiene_pedidos:
            j_productos_repo.j_cambiar_estado(id_producto, "INACTIVO")
            return {
                "mensaje": "El producto tiene movimientos asociados (recetas o pedidos). Se realizó borrado lógico (estado INACTIVO).",
                "tipo_eliminacion": "LOGICA",
                "id": id_producto
            }
        else:
            j_productos_repo.j_eliminar_fisico(id_producto)
            return {
                "mensaje": "Producto eliminado físicamente con éxito.",
                "tipo_eliminacion": "FISICA",
                "id": id_producto
            }

    def j_calcular_costo_y_margen(self, id_producto: str) -> JProductoCostoMargenResponse:
        """
        Calcula el costo de producción a partir de la receta (fichas técnicas) y
        el margen de ganancia frente al precio de venta (RF06).
        """
        prod = self.j_obtener_por_id(id_producto)
        items_receta = j_recetas_repo.j_obtener_por_producto(id_producto)

        costo_total = 0.0
        detalles_insumo: List[JInsumoDetalleCosto] = []

        for item in items_receta:
            insumo = j_insumos_repo.j_obtener_por_id(item["id_insumo"])
            if insumo:
                costo_u = float(insumo.get("costo_unitario", 0.0))
                subtotal = float(item["cantidad"]) * costo_u
                costo_total += subtotal
                detalles_insumo.append(
                    JInsumoDetalleCosto(
                        id_insumo=insumo["id"],
                        nombre_insumo=insumo["nombre"],
                        unidad_medida=insumo.get("unidad_medida", "unidad"),
                        cantidad_receta=float(item["cantidad"]),
                        costo_unitario=round(costo_u, 2),
                        subtotal_costo=round(subtotal, 2)
                    )
                )

        precio_venta = float(prod.get("precio_venta", 0.0))
        costo_total = round(costo_total, 2)
        margen = round(precio_venta - costo_total, 2)
        porcentaje_margen = round((margen / precio_venta) * 100, 2) if precio_venta > 0 else 0.0

        return JProductoCostoMargenResponse(
            id_producto=prod["id"],
            codigo=prod["codigo"],
            nombre_producto=prod["nombre"],
            precio_venta=precio_venta,
            costo_produccion=costo_total,
            margen_ganancia=margen,
            porcentaje_margen=porcentaje_margen,
            detalle_insumos=detalles_insumo
        )


j_productos_service = JProductosService()
