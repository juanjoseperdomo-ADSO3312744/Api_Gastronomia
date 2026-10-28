from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_proveedores_schema import JProveedorCreate, JProveedorUpdate, JProveedorResponse
from app.schemas.j_compras_schema import JCompraResponse
from app.services.j_proveedores_service import j_proveedores_service
from app.core.j_security import j_requiere_roles

j_proveedores_router = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"],
    dependencies=[Depends(j_requiere_roles(["ADMIN"]))]
)


@j_proveedores_router.get(
    "",
    response_model=List[JProveedorResponse],
    summary="Listar todos los proveedores"
)
def j_listar_proveedores(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200)
):
    return j_proveedores_service.j_listar_proveedores(salto=salto, limite=limite)


@j_proveedores_router.get(
    "/{id}/compras",
    response_model=List[JCompraResponse],
    summary="Consultar historial de compras realizadas a un proveedor"
)
def j_compras_por_proveedor(id: str):
    return j_proveedores_service.j_obtener_compras_proveedor(id)


@j_proveedores_router.get(
    "/{id}",
    response_model=JProveedorResponse,
    summary="Obtener un proveedor por ID"
)
def j_obtener_proveedor(id: str):
    return j_proveedores_service.j_obtener_por_id(id)


@j_proveedores_router.post(
    "",
    response_model=JProveedorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo proveedor"
)
def j_crear_proveedor(datos: JProveedorCreate):
    return j_proveedores_service.j_crear_proveedor(datos)


@j_proveedores_router.put(
    "/{id}",
    response_model=JProveedorResponse,
    summary="Actualizar un proveedor"
)
def j_actualizar_proveedor(id: str, datos: JProveedorUpdate):
    return j_proveedores_service.j_actualizar_proveedor(id, datos)


@j_proveedores_router.delete(
    "/{id}",
    summary="Eliminar proveedor (Aplica RN04 borrado lógico si tiene compras registradas)"
)
def j_eliminar_proveedor(id: str):
    return j_proveedores_service.j_eliminar_proveedor(id)
