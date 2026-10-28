from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_calificaciones_schema import (
    JCalificacionCreate,
    JCalificacionResponse,
    JCalificacionProductoResumen
)
from app.services.j_calificaciones_service import j_calificaciones_service
from app.core.j_security import j_requiere_roles

j_calificaciones_router = APIRouter(
    prefix="/calificaciones",
    tags=["Calificaciones (MongoDB)"],
    dependencies=[Depends(j_requiere_roles(["ADMIN", "CAJERO"]))]
)


@j_calificaciones_router.get(
    "/producto/{id_producto}",
    response_model=JCalificacionProductoResumen,
    summary="Consultar calificaciones y calificación promedio de un producto (RF12)"
)
def j_calificaciones_por_producto(id_producto: str):
    return j_calificaciones_service.j_obtener_por_producto(id_producto)


@j_calificaciones_router.get(
    "",
    response_model=List[JCalificacionResponse],
    summary="Listar todas las evaluaciones de clientes registradas"
)
def j_listar_calificaciones(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200)
):
    return j_calificaciones_service.j_listar_calificaciones(salto=salto, limite=limite)


@j_calificaciones_router.get(
    "/{id}",
    response_model=JCalificacionResponse,
    summary="Obtener una calificación por ID"
)
def j_obtener_calificacion(id: str):
    return j_calificaciones_service.j_obtener_por_id(id)


@j_calificaciones_router.post(
    "",
    response_model=JCalificacionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar calificación de un cliente sobre su pedido y productos consumidos"
)
def j_crear_calificacion(datos: JCalificacionCreate):
    return j_calificaciones_service.j_crear_calificacion(datos)


@j_calificaciones_router.put(
    "/{id}",
    response_model=JCalificacionResponse,
    summary="Actualizar una calificación existente"
)
def j_actualizar_calificacion(id: str, datos: dict):
    return j_calificaciones_service.j_actualizar_calificacion(id, datos)


@j_calificaciones_router.delete(
    "/{id}",
    summary="Eliminar una calificación"
)
def j_eliminar_calificacion(id: str):
    return j_calificaciones_service.j_eliminar_calificacion(id)
