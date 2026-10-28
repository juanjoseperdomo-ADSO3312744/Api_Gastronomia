from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_clientes_schema import JClienteCreate, JClienteUpdate, JClienteResponse
from app.schemas.j_pedidos_schema import JPedidoResponse
from app.services.j_clientes_service import j_clientes_service
from app.core.j_security import j_requiere_roles

j_clientes_router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
    dependencies=[Depends(j_requiere_roles(["ADMIN", "CAJERO"]))]
)


@j_clientes_router.get(
    "",
    response_model=List[JClienteResponse],
    summary="Listar todos los clientes (ADMIN, CAJERO)"
)
def j_listar_clientes(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200)
):
    return j_clientes_service.j_listar_clientes(salto=salto, limite=limite)


@j_clientes_router.get(
    "/{id}/pedidos",
    response_model=List[JPedidoResponse],
    summary="Consultar historial de pedidos de un cliente (ADMIN, CAJERO)"
)
def j_pedidos_por_cliente(id: str):
    return j_clientes_service.j_obtener_pedidos_cliente(id)


@j_clientes_router.get(
    "/{id}",
    response_model=JClienteResponse,
    summary="Obtener un cliente por ID (ADMIN, CAJERO)"
)
def j_obtener_cliente(id: str):
    return j_clientes_service.j_obtener_por_id(id)


@j_clientes_router.post(
    "",
    response_model=JClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo cliente (ADMIN, CAJERO)"
)
def j_crear_cliente(datos: JClienteCreate):
    return j_clientes_service.j_crear_cliente(datos)


@j_clientes_router.put(
    "/{id}",
    response_model=JClienteResponse,
    summary="Actualizar un cliente (ADMIN, CAJERO)"
)
def j_actualizar_cliente(id: str, datos: JClienteUpdate):
    return j_clientes_service.j_actualizar_cliente(id, datos)


@j_clientes_router.delete(
    "/{id}",
    summary="Eliminar cliente (ADMIN, CAJERO - Aplica RN04 borrado lógico si tiene pedidos asociados)"
)
def j_eliminar_cliente(id: str):
    return j_clientes_service.j_eliminar_cliente(id)
