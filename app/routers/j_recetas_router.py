from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_recetas_schema import JRecetaCreate, JRecetaUpdate, JRecetaResponse
from app.services.j_recetas_service import j_recetas_service
from app.core.j_security import j_requiere_roles

j_recetas_router = APIRouter(
    prefix="/recetas",
    tags=["Recetas (Fichas Técnicas)"],
    dependencies=[Depends(j_requiere_roles(["ADMIN", "COCINERO"]))]
)


@j_recetas_router.get(
    "",
    response_model=List[JRecetaResponse],
    summary="Listar todos los ítems de recetas registrados"
)
def j_listar_recetas(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200)
):
    return j_recetas_service.j_listar_recetas(salto=salto, limite=limite)


@j_recetas_router.get(
    "/{id}",
    response_model=JRecetaResponse,
    summary="Obtener un ítem de receta por ID"
)
def j_obtener_receta(id: str):
    return j_recetas_service.j_obtener_por_id(id)


@j_recetas_router.post(
    "",
    response_model=JRecetaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Asociar un insumo y cantidad a un producto (RF05)"
)
def j_crear_receta(datos: JRecetaCreate):
    return j_recetas_service.j_crear_item_receta(datos)


@j_recetas_router.put(
    "/{id}",
    response_model=JRecetaResponse,
    summary="Actualizar un ítem de receta"
)
def j_actualizar_receta(id: str, datos: JRecetaUpdate):
    return j_recetas_service.j_actualizar_item_receta(id, datos)


@j_recetas_router.delete(
    "/{id}",
    summary="Eliminar un ítem de receta"
)
def j_eliminar_receta(id: str):
    return j_recetas_service.j_eliminar_item_receta(id)
