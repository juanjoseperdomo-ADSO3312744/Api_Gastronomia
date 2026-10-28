from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_compras_schema import JCompraCreate, JCompraUpdate, JCompraResponse
from app.services.j_compras_service import j_compras_service
from app.core.j_security import j_requiere_roles

j_compras_router = APIRouter(
    prefix="/compras",
    tags=["Compras a Proveedores"],
    dependencies=[Depends(j_requiere_roles(["ADMIN"]))]
)


@j_compras_router.get(
    "",
    response_model=List[JCompraResponse],
    summary="Listar compras de insumos registradas"
)
def j_listar_compras(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200)
):
    return j_compras_service.j_listar_compras(salto=salto, limite=limite)


@j_compras_router.get(
    "/{id}",
    response_model=JCompraResponse,
    summary="Obtener una compra por ID con su detalle de insumos"
)
def j_obtener_compra(id: str):
    return j_compras_service.j_obtener_por_id(id)


@j_compras_router.post(
    "",
    response_model=JCompraResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una compra de insumos (Aplica RN02: incrementa existencias y actualiza costo)"
)
def j_registrar_compra(
    datos: JCompraCreate,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN"]))
):
    return j_compras_service.j_registrar_compra(datos, id_usuario=usuario_actual["id"])


@j_compras_router.put(
    "/{id}",
    response_model=JCompraResponse,
    summary="Actualizar información básica de una compra"
)
def j_actualizar_compra(id: str, datos: JCompraUpdate):
    return j_compras_service.j_actualizar_compra(id, datos)


@j_compras_router.delete(
    "/{id}",
    summary="Eliminar registro de compra"
)
def j_eliminar_compra(id: str):
    return j_compras_service.j_eliminar_compra(id)
