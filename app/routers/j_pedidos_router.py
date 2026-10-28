from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_pedidos_schema import (
    JPedidoCreate,
    JPedidoUpdate,
    JPedidoEstadoUpdate,
    JPedidoResponse
)
from app.services.j_pedidos_service import j_pedidos_service
from app.core.j_security import j_requiere_roles

j_pedidos_router = APIRouter(prefix="/pedidos", tags=["Pedidos y Ventas"])


@j_pedidos_router.get(
    "/estado/{estado}",
    response_model=List[JPedidoResponse],
    summary="Consultar pedidos filtrados por estado (ADMIN, CAJERO, COCINERO)"
)
def j_pedidos_por_estado(
    estado: str,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN", "CAJERO", "COCINERO"]))
):
    return j_pedidos_service.j_obtener_por_estado(estado)


@j_pedidos_router.patch(
    "/{id}/estado",
    response_model=JPedidoResponse,
    summary="Cambiar estado del pedido (ADMIN, CAJERO, COCINERO - Aplica RN03 y RN05)"
)
def j_cambiar_estado_pedido(
    id: str,
    datos: JPedidoEstadoUpdate,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN", "CAJERO", "COCINERO"]))
):
    return j_pedidos_service.j_cambiar_estado(id, datos.estado.value)


@j_pedidos_router.get(
    "",
    response_model=List[JPedidoResponse],
    summary="Listar todos los pedidos (ADMIN, CAJERO)"
)
def j_listar_pedidos(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200),
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN", "CAJERO"]))
):
    return j_pedidos_service.j_listar_pedidos(salto=salto, limite=limite)


@j_pedidos_router.get(
    "/{id}",
    response_model=JPedidoResponse,
    summary="Obtener un pedido por ID con su detalle (ADMIN, CAJERO, COCINERO)"
)
def j_obtener_pedido(
    id: str,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN", "CAJERO", "COCINERO"]))
):
    return j_pedidos_service.j_obtener_por_id(id)


@j_pedidos_router.post(
    "",
    response_model=JPedidoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo pedido (ADMIN, CAJERO - Aplica RN01)"
)
def j_crear_pedido(
    datos: JPedidoCreate,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN", "CAJERO"]))
):
    return j_pedidos_service.j_crear_pedido(datos, id_usuario=usuario_actual["id"])


@j_pedidos_router.put(
    "/{id}",
    response_model=JPedidoResponse,
    summary="Actualizar pedido (ADMIN, CAJERO - Aplica RN05 si está entregado o anulado)"
)
def j_actualizar_pedido(
    id: str,
    datos: JPedidoUpdate,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN", "CAJERO"]))
):
    return j_pedidos_service.j_actualizar_pedido(id, datos)


@j_pedidos_router.delete(
    "/{id}",
    summary="Eliminar pedido (ADMIN, CAJERO - Valida RN05)"
)
def j_eliminar_pedido(
    id: str,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN", "CAJERO"]))
):
    return j_pedidos_service.j_eliminar_pedido(id)
