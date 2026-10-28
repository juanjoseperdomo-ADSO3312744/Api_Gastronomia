from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from collections import defaultdict
from fastapi import HTTPException, status

from app.repositories.j_pedidos_repository import j_pedidos_repo
from app.repositories.j_clientes_repository import j_clientes_repo
from app.repositories.j_usuarios_repository import j_usuarios_repo
from app.repositories.j_productos_repository import j_productos_repo
from app.repositories.j_recetas_repository import j_recetas_repo
from app.repositories.j_insumos_repository import j_insumos_repo
from app.schemas.j_pedidos_schema import JPedidoCreate, JPedidoUpdate


class JPedidosService:
    def _j_enriquecer_pedido(self, pedido: Dict[str, Any]) -> Dict[str, Any]:
        """Añade datos legibles del cliente, usuario y nombres de productos al pedido."""
        if pedido:
            cli = j_clientes_repo.j_obtener_por_id(str(pedido.get("id_cliente")))
            usr = j_usuarios_repo.j_obtener_por_id(str(pedido.get("id_usuario")))
            pedido["cliente_nombre"] = f"{cli.get('nombres', '')} {cli.get('apellidos', '')}".strip() if cli else "Cliente desconocido"
            pedido["usuario_nombre"] = f"{usr.get('nombres', '')} {usr.get('apellidos', '')}".strip() if usr else "Sistema"

            for item in pedido.get("detalle", []):
                prod = j_productos_repo.j_obtener_por_id(str(item.get("id_producto")))
                item["nombre_producto"] = prod["nombre"] if prod else "Producto desconocido"
        return pedido

    def j_crear_pedido(self, datos: JPedidoCreate, id_usuario: str) -> Dict[str, Any]:
        """
        Crea un nuevo pedido aplicando la regla de negocio RN01:
        El subtotal de cada ítem = cantidad * precio_unitario y el total = suma de subtotales.
        Los precios se obtienen de la base de datos, no del cliente.
        """
        # Validar cliente
        cli = j_clientes_repo.j_obtener_por_id(datos.id_cliente)
        if not cli:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID '{datos.id_cliente}' no encontrado."
            )
        if cli.get("estado") != "ACTIVO":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pueden registrar pedidos para clientes inactivos."
            )

        items_procesados = []
        total_acumulado = 0.0

        for item in datos.detalle:
            prod = j_productos_repo.j_obtener_por_id(item.id_producto)
            if not prod:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID '{item.id_producto}' no existe."
                )

            if prod.get("estado") == "INACTIVO":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El producto '{prod['nombre']}' se encuentra INACTIVO."
                )

            # RN01: Obtener precio unitario del catálogo y calcular subtotal
            precio_u = float(prod.get("precio_venta", 0.0))
            cant = float(item.cantidad)
            subtotal = round(cant * precio_u, 2)
            total_acumulado += subtotal

            items_procesados.append({
                "id_producto": str(item.id_producto),
                "cantidad": cant,
                "precio_unitario": precio_u,
                "subtotal": subtotal
            })

        fecha_ahora = datetime.now(timezone.utc).isoformat()

        doc_pedido = {
            "fecha_pedido": fecha_ahora,
            "id_cliente": str(datos.id_cliente),
            "id_usuario": str(id_usuario),
            "tipo_pedido": datos.tipo_pedido.value,
            "estado": "PENDIENTE",
            "total": round(total_acumulado, 2),
            "detalle": items_procesados,
            "observaciones": datos.observaciones or ""
        }

        pedido_creado = j_pedidos_repo.j_crear(doc_pedido)
        return self._j_enriquecer_pedido(pedido_creado)

    def j_obtener_por_id(self, id_pedido: str) -> Dict[str, Any]:
        pedido = j_pedidos_repo.j_obtener_por_id(id_pedido)
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido con ID '{id_pedido}' no encontrado."
            )
        return self._j_enriquecer_pedido(pedido)

    def j_listar_pedidos(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        pedidos = j_pedidos_repo.j_obtener_todos(salto=salto, limite=limite, orden=[("fecha_pedido", -1)])
        return [self._j_enriquecer_pedido(p) for p in pedidos]

    def j_obtener_por_estado(self, estado: str) -> List[Dict[str, Any]]:
        pedidos = j_pedidos_repo.j_obtener_por_estado(estado)
        return [self._j_enriquecer_pedido(p) for p in pedidos]

    def j_actualizar_pedido(self, id_pedido: str, datos: JPedidoUpdate) -> Dict[str, Any]:
        """
        Actualiza un pedido existente.
        Aplica la regla de negocio RN05:
        Un pedido ENTREGADO o ANULADO no puede modificarse.
        """
        pedido_existente = j_pedidos_repo.j_obtener_por_id(id_pedido)
        if not pedido_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido con ID '{id_pedido}' no encontrado."
            )

        # Regla RN05: Validar inmutabilidad de pedidos finalizados
        if pedido_existente.get("estado") in ["ENTREGADO", "ANULADO"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Regla de negocio RN05: Un pedido con estado '{pedido_existente.get('estado')}' no puede ser modificado."
            )

        datos_act: Dict[str, Any] = {}
        if datos.id_cliente is not None:
            if not j_clientes_repo.j_obtener_por_id(datos.id_cliente):
                raise HTTPException(status_code=404, detail="Cliente no existe.")
            datos_act["id_cliente"] = str(datos.id_cliente)

        if datos.tipo_pedido is not None:
            datos_act["tipo_pedido"] = datos.tipo_pedido.value

        if datos.observaciones is not None:
            datos_act["observaciones"] = datos.observaciones

        # Si se actualiza el detalle, recalcular subtotales y total (RN01)
        if datos.detalle is not None:
            items_procesados = []
            total_acumulado = 0.0
            for item in datos.detalle:
                prod = j_productos_repo.j_obtener_por_id(item.id_producto)
                if not prod:
                    raise HTTPException(status_code=404, detail=f"Producto '{item.id_producto}' no existe.")
                precio_u = float(prod.get("precio_venta", 0.0))
                cant = float(item.cantidad)
                subtotal = round(cant * precio_u, 2)
                total_acumulado += subtotal
                items_procesados.append({
                    "id_producto": str(item.id_producto),
                    "cantidad": cant,
                    "precio_unitario": precio_u,
                    "subtotal": subtotal
                })
            datos_act["detalle"] = items_procesados
            datos_act["total"] = round(total_acumulado, 2)

        actualizado = j_pedidos_repo.j_actualizar(id_pedido, datos_act)
        return self._j_enriquecer_pedido(actualizado)

    def j_cambiar_estado(self, id_pedido: str, nuevo_estado: str) -> Dict[str, Any]:
        """
        Cambia el estado de un pedido aplicando las reglas de negocio RN03 y RN05:
        - RN05: Un pedido ENTREGADO o ANULADO no puede modificarse.
        - RN03: Al cambiar a ENTREGADO, se descuentan del inventario los insumos según la receta.
                Si no hay existencias suficientes, responde con HTTP 409.
        """
        pedido = j_pedidos_repo.j_obtener_por_id(id_pedido)
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido con ID '{id_pedido}' no encontrado."
            )

        estado_actual = pedido.get("estado", "")
        nuevo_estado_upper = nuevo_estado.upper()

        # RN05: Pedidos ya finalizados no se pueden alterar
        if estado_actual in ["ENTREGADO", "ANULADO"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Regla de negocio RN05: El pedido ya se encuentra en estado '{estado_actual}' y no permite cambios."
            )

        # RN03: Si cambia a ENTREGADO, verificar y descontar existencias de insumos según recetas
        if nuevo_estado_upper == "ENTREGADO":
            insumos_requeridos = defaultdict(float)

            # Calcular el total de insumos necesarios sumando recetas de todos los productos ordenados
            for item in pedido.get("detalle", []):
                id_prod = item["id_producto"]
                cant_prod = float(item["cantidad"])
                receta_items = j_recetas_repo.j_obtener_por_producto(id_prod)

                for r_item in receta_items:
                    insumo_id = r_item["id_insumo"]
                    cant_insumo_unitaria = float(r_item["cantidad"])
                    insumos_requeridos[insumo_id] += cant_insumo_unitaria * cant_prod

            # Verificar existencias de cada insumo antes de hacer cualquier descuento
            for insumo_id, cant_necesaria in insumos_requeridos.items():
                insumo = j_insumos_repo.j_obtener_por_id(insumo_id)
                nombre_insumo = insumo.get("nombre", f"ID {insumo_id}") if insumo else f"ID {insumo_id}"
                stock_actual = float(insumo.get("stock_actual", 0.0)) if insumo else 0.0

                if stock_actual < cant_necesaria:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=(
                            f"Regla de negocio RN03 (Existencias insuficientes): El insumo '{nombre_insumo}' "
                            f"tiene stock actual de {stock_actual}, pero se requieren {cant_necesaria} "
                            f"para completar el pedido. No se puede entregar el pedido."
                        )
                    )

            # Si todos los insumos tienen stock suficiente, descontar inventario
            for insumo_id, cant_necesaria in insumos_requeridos.items():
                j_insumos_repo.j_descontar_stock(insumo_id, cant_necesaria)

        # Actualizar estado del pedido
        pedido_actualizado = j_pedidos_repo.j_actualizar_estado(id_pedido, nuevo_estado_upper)
        return self._j_enriquecer_pedido(pedido_actualizado)

    def j_eliminar_pedido(self, id_pedido: str) -> Dict[str, Any]:
        """
        Elimina o anula un pedido. Si está entregado, no puede eliminarse (RN05).
        """
        pedido = j_pedidos_repo.j_obtener_por_id(id_pedido)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")

        if pedido.get("estado") == "ENTREGADO":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un pedido ya ENTREGADO no puede eliminarse físicamente."
            )

        j_pedidos_repo.j_eliminar_fisico(id_pedido)
        return {"mensaje": "Pedido eliminado con éxito.", "id": id_pedido}


j_pedidos_service = JPedidosService()
