from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from app.repositories.j_calificaciones_repository import j_calificaciones_repo
from app.repositories.j_pedidos_repository import j_pedidos_repo
from app.repositories.j_clientes_repository import j_clientes_repo
from app.repositories.j_productos_repository import j_productos_repo
from app.schemas.j_calificaciones_schema import (
    JCalificacionCreate,
    JCalificacionProductoResumen,
    JCalificacionProductoDetalle
)


class JCalificacionesService:
    def _j_enriquecer_calificacion(self, cal: Dict[str, Any]) -> Dict[str, Any]:
        if cal:
            cli = j_clientes_repo.j_obtener_por_id(str(cal.get("id_cliente")))
            cal["cliente_nombre"] = f"{cli.get('nombres', '')} {cli.get('apellidos', '')}".strip() if cli else "Cliente desconocido"
        return cal

    def j_crear_calificacion(self, datos: JCalificacionCreate) -> Dict[str, Any]:
        """
        Registra una calificación no estructurada en MongoDB (RF12).
        """
        # Validar pedido
        pedido = j_pedidos_repo.j_obtener_por_id(datos.id_pedido)
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido con ID '{datos.id_pedido}' no encontrado."
            )

        # Validar cliente
        cli = j_clientes_repo.j_obtener_por_id(datos.id_cliente)
        if not cli:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID '{datos.id_cliente}' no encontrado."
            )

        # Enriquecer nombres de productos calificados si no vinieron
        prods_calificados = []
        for p in datos.productos:
            prod_db = j_productos_repo.j_obtener_por_id(p.id_producto)
            nom = prod_db["nombre"] if prod_db else p.nombre or "Producto"
            prods_calificados.append({
                "id_producto": str(p.id_producto),
                "nombre": nom,
                "calificacion": int(p.calificacion)
            })

        fecha = datos.fecha or datetime.now(timezone.utc).isoformat()

        doc = {
            "id_pedido": str(datos.id_pedido),
            "id_cliente": str(datos.id_cliente),
            "fecha": fecha,
            "calificacion_servicio": int(datos.calificacion_servicio),
            "comentario": datos.comentario or "",
            "productos": prods_calificados
        }

        creado = j_calificaciones_repo.j_crear(doc)
        return self._j_enriquecer_calificacion(creado)

    def j_obtener_por_id(self, id_calificacion: str) -> Dict[str, Any]:
        cal = j_calificaciones_repo.j_obtener_por_id(id_calificacion)
        if not cal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Calificación con ID '{id_calificacion}' no encontrada."
            )
        return self._j_enriquecer_calificacion(cal)

    def j_listar_calificaciones(self, salto: int = 0, limite: int = 100) -> List[Dict[str, Any]]:
        calificaciones = j_calificaciones_repo.j_obtener_todos(salto=salto, limite=limite, orden=[("fecha", -1)])
        return [self._j_enriquecer_calificacion(c) for c in calificaciones]

    def j_actualizar_calificacion(self, id_calificacion: str, datos: dict) -> Dict[str, Any]:
        cal = j_calificaciones_repo.j_obtener_por_id(id_calificacion)
        if not cal:
            raise HTTPException(status_code=404, detail="Calificación no encontrada.")
        act = j_calificaciones_repo.j_actualizar(id_calificacion, datos)
        return self._j_enriquecer_calificacion(act)

    def j_eliminar_calificacion(self, id_calificacion: str) -> Dict[str, Any]:
        cal = j_calificaciones_repo.j_obtener_por_id(id_calificacion)
        if not cal:
            raise HTTPException(status_code=404, detail="Calificación no encontrada.")
        j_calificaciones_repo.j_eliminar_fisico(id_calificacion)
        return {"mensaje": "Calificación eliminada con éxito.", "id": id_calificacion}

    def j_obtener_por_producto(self, id_producto: str) -> JCalificacionProductoResumen:
        """
        Retorna las calificaciones individuales y el promedio de calificación de un producto (RF12).
        """
        prod = j_productos_repo.j_obtener_por_id(id_producto)
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID '{id_producto}' no existe."
            )

        documentos = j_calificaciones_repo.j_obtener_por_producto(id_producto)
        detalles: List[JCalificacionProductoDetalle] = []
        puntuaciones: List[int] = []

        for doc in documentos:
            cli = j_clientes_repo.j_obtener_por_id(str(doc.get("id_cliente")))
            cli_nombre = f"{cli.get('nombres', '')} {cli.get('apellidos', '')}".strip() if cli else "Cliente"

            for p_item in doc.get("productos", []):
                if str(p_item.get("id_producto")) == str(id_producto):
                    calif = int(p_item.get("calificacion", 0))
                    puntuaciones.append(calif)
                    detalles.append(
                        JCalificacionProductoDetalle(
                            id_calificacion=doc["id"],
                            id_pedido=doc["id_pedido"],
                            id_cliente=doc["id_cliente"],
                            cliente_nombre=cli_nombre,
                            fecha=str(doc.get("fecha", "")),
                            calificacion=calif,
                            comentario=doc.get("comentario", "")
                        )
                    )

        total = len(puntuaciones)
        promedio = round(sum(puntuaciones) / total, 2) if total > 0 else 0.0

        return JCalificacionProductoResumen(
            id_producto=prod["id"],
            nombre_producto=prod["nombre"],
            promedio_calificacion=promedio,
            total_calificaciones=total,
            calificaciones=detalles
        )


j_calificaciones_service = JCalificacionesService()
