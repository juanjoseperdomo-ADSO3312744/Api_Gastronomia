from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from app.repositories.j_compras_repository import j_compras_repo
from app.repositories.j_proveedores_repository import j_proveedores_repo
from app.repositories.j_insumos_repository import j_insumos_repo
from app.repositories.j_usuarios_repository import j_usuarios_repo
from app.schemas.j_compras_schema import JCompraCreate, JCompraUpdate


class JComprasService:
    def _j_enriquecer_compra(self, compra: Dict[str, Any]) -> Dict[str, Any]:
        """Añade datos legibles del proveedor, usuario y nombres de insumos al documento."""
        if compra:
            prov = j_proveedores_repo.j_obtener_por_id(str(compra.get("id_proveedor")))
            usr = j_usuarios_repo.j_obtener_por_id(str(compra.get("id_usuario")))
            compra["proveedor_razon_social"] = prov["razon_social"] if prov else "Proveedor desconocido"
            compra["usuario_nombre"] = f"{usr.get('nombres', '')} {usr.get('apellidos', '')}".strip() if usr else "Sistema"

            for item in compra.get("detalle", []):
                ins = j_insumos_repo.j_obtener_por_id(str(item.get("id_insumo")))
                item["nombre_insumo"] = ins["nombre"] if ins else "Insumo desconocido"
                item["unidad_medida"] = ins.get("unidad_medida", "unidad") if ins else "unidad"
        return compra

    def j_registrar_compra(self, datos: JCompraCreate, id_usuario: str) -> Dict[str, Any]:
        """
        Registra una compra y ejecuta la regla de negocio RN02:
        Al registrar una compra, se incrementa el stock_actual de cada insumo y se actualiza su costo_unitario.
        """
        # Validar proveedor
        prov = j_proveedores_repo.j_obtener_por_id(datos.id_proveedor)
        if not prov:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor con ID '{datos.id_proveedor}' no encontrado."
            )

        # Validar factura no duplicada
        if j_compras_repo.j_buscar_por_numero_factura(datos.numero_factura):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una compra registrada con la factura '{datos.numero_factura}'."
            )

        # Procesar y validar insumos del detalle
        items_procesados = []
        total_acumulado = 0.0

        for item in datos.detalle:
            ins = j_insumos_repo.j_obtener_por_id(item.id_insumo)
            if not ins:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Insumo con ID '{item.id_insumo}' no existe."
                )

            cant = float(item.cantidad)
            costo_u = float(item.costo_unitario)
            subtotal = round(cant * costo_u, 2)
            total_acumulado += subtotal

            items_procesados.append({
                "id_insumo": str(item.id_insumo),
                "cantidad": cant,
                "costo_unitario": costo_u,
                "subtotal": subtotal
            })

        fecha_compra = datos.fecha_compra or datetime.now(timezone.utc).isoformat()

        doc_compra = {
            "numero_factura": datos.numero_factura.strip(),
            "fecha_compra": fecha_compra,
            "id_proveedor": str(datos.id_proveedor),
            "id_usuario": str(id_usuario),
            "total": round(total_acumulado, 2),
            "detalle": items_procesados
        }

        # Guardar compra
        compra_creada = j_compras_repo.j_crear(doc_compra)

        # Regla RN02: Incrementar existencias y actualizar costo unitario en insumos
        for item in items_procesados:
            j_insumos_repo.j_incrementar_stock_y_costo(
                id_insumo=item["id_insumo"],
                cantidad=item["cantidad"],
                nuevo_costo=item["costo_unitario"]
            )

        return self._j_enriquecer_compra(compra_creada)

    def j_obtener_por_id(self, id_compra: str) -> Dict[str, Any]:
        compra = j_compras_repo.j_obtener_por_id(id_compra)
        if not compra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra con ID '{id_compra}' no encontrada."
            )
        return self._j_enriquecer_compra(compra)

    def j_listar_compras(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        compras = j_compras_repo.j_obtener_todos(salto=salto, limite=limite, orden=[("fecha_compra", -1)])
        return [self._j_enriquecer_compra(c) for c in compras]

    def j_actualizar_compra(self, id_compra: str, datos: JCompraUpdate) -> Dict[str, Any]:
        compra = j_compras_repo.j_obtener_por_id(id_compra)
        if not compra:
            raise HTTPException(status_code=404, detail="Compra no encontrada.")

        datos_act = datos.model_dump(exclude_unset=True)
        if "numero_factura" in datos_act and datos_act["numero_factura"]:
            nuevo_num = datos_act["numero_factura"].strip()
            encontrado = j_compras_repo.j_buscar_por_numero_factura(nuevo_num)
            if encontrado and encontrado["id"] != id_compra:
                raise HTTPException(status_code=409, detail=f"La factura '{nuevo_num}' ya está registrada.")
            datos_act["numero_factura"] = nuevo_num

        if "id_proveedor" in datos_act and datos_act["id_proveedor"]:
            if not j_proveedores_repo.j_obtener_por_id(datos_act["id_proveedor"]):
                raise HTTPException(status_code=404, detail="Proveedor no encontrado.")

        act = j_compras_repo.j_actualizar(id_compra, datos_act)
        return self._j_enriquecer_compra(act)

    def j_eliminar_compra(self, id_compra: str) -> Dict[str, Any]:
        compra = j_compras_repo.j_obtener_por_id(id_compra)
        if not compra:
            raise HTTPException(status_code=404, detail="Compra no encontrada.")
        j_compras_repo.j_eliminar_fisico(id_compra)
        return {"mensaje": "Compra eliminada con éxito.", "id": id_compra}


j_compras_service = JComprasService()
