from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_categorias_schema import JCategoriaCreate, JCategoriaUpdate, JCategoriaResponse
from app.services.j_categorias_service import j_categorias_service
from app.core.j_security import j_obtener_usuario_actual, j_requiere_roles

j_categorias_router = APIRouter(prefix="/categorias", tags=["Categorías"])


@j_categorias_router.get(
    "",
    response_model=List[JCategoriaResponse],
    summary="Listar categorías de productos (Todos autenticados)"
)
def j_listar_categorias(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200),
    usuario_actual: dict = Depends(j_obtener_usuario_actual)
):
    return j_categorias_service.j_listar_categorias(salto=salto, limite=limite)


@j_categorias_router.get(
    "/{id}",
    response_model=JCategoriaResponse,
    summary="Obtener una categoría por ID (Todos autenticados)"
)
def j_obtener_categoria(
    id: str,
    usuario_actual: dict = Depends(j_obtener_usuario_actual)
):
    return j_categorias_service.j_obtener_por_id(id)


@j_categorias_router.post(
    "",
    response_model=JCategoriaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva categoría (Solo ADMIN)"
)
def j_crear_categoria(
    datos: JCategoriaCreate,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN"]))
):
    return j_categorias_service.j_crear_categoria(datos)


@j_categorias_router.put(
    "/{id}",
    response_model=JCategoriaResponse,
    summary="Actualizar categoría existente (Solo ADMIN)"
)
def j_actualizar_categoria(
    id: str,
    datos: JCategoriaUpdate,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN"]))
):
    return j_categorias_service.j_actualizar_categoria(id, datos)


@j_categorias_router.delete(
    "/{id}",
    summary="Eliminar categoría (Solo ADMIN - Aplica RN04 borrado lógico si tiene productos asociados)"
)
def j_eliminar_categoria(
    id: str,
    usuario_actual: dict = Depends(j_requiere_roles(["ADMIN"]))
):
    return j_categorias_service.j_eliminar_categoria(id)
