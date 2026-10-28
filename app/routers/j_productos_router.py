from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_productos_schema import (
    JProductoCreate,
    JProductoUpdate,
    JProductoResponse,
    JProductoCostoMargenResponse
)
from app.schemas.j_recetas_schema import JRecetaProductoDetalleResponse
from app.services.j_productos_service import j_productos_service
from app.services.j_recetas_service import j_recetas_service
from app.core.j_security import j_obtener_usuario_actual, j_requiere_roles

j_productos_router = APIRouter(prefix="/productos", tags=["Productos"])


@j_productos_router.get(
    "",
    response_model=List[JProductoResponse],
    summary="Listar catálogo de productos (Todos autenticados)"
)
def j_listar_productos(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200),
    usuario_actual: dict = Depends(j_obtener_usuario_actual)
):
    return j_productos_service.j_listar_productos(salto=salto, limite=limite)


@j_productos_router.get(
    "/categoria/{id_categoria}",
    response_model=List[JProductoResponse],
    summary="Consultar productos de una categoría (Todos autenticados)"
)
def j_productos_por_categoria(
    id_categoria: str,
    usuario_actual: dict = Depends(j_obtener_usuario_actual)
):
    return j_productos_service.j_obtener_por_categoria(id_categoria)


@j_productos_router.get(
    "/{id}/receta",
    response_model=JRecetaProductoDetalleResponse,
    summary="Consultar insumos y cantidades de la receta de un producto (ADMIN, COCINERO)"
)
def j_receta_de_producto(
    id: str,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN", "COCINERO"]))
):
    return j_recetas_service.j_obtener_receta_producto(id)


@j_productos_router.get(
    "/{id}/costo",
    response_model=JProductoCostoMargenResponse,
    summary="Calcular costo de producción y margen de ganancia (ADMIN, COCINERO)"
)
def j_costo_de_producto(
    id: str,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN", "COCINERO"]))
):
    return j_productos_service.j_calcular_costo_y_margen(id)


@j_productos_router.get(
    "/{id}",
    response_model=JProductoResponse,
    summary="Obtener un producto por ID (Todos autenticados)"
)
def j_obtener_producto(
    id: str,
    usuario_actual: dict = Depends(j_obtener_usuario_actual)
):
    return j_productos_service.j_obtener_por_id(id)


@j_productos_router.post(
    "",
    response_model=JProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto (Solo ADMIN)"
)
def j_crear_producto(
    datos: JProductoCreate,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN"]))
):
    return j_productos_service.j_crear_producto(datos)


@j_productos_router.put(
    "/{id}",
    response_model=JProductoResponse,
    summary="Actualizar producto existente (Solo ADMIN)"
)
def j_actualizar_producto(
    id: str,
    datos: JProductoUpdate,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN"]))
):
    return j_productos_service.j_actualizar_producto(id, datos)


@j_productos_router.delete(
    "/{id}",
    summary="Eliminar producto (Solo ADMIN - Aplica RN04 borrado lógico si tiene recetas o pedidos)"
)
def j_eliminar_producto(
    id: str,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN"]))
):
    return j_productos_service.j_eliminar_producto(id)
