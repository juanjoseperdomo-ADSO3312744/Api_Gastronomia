from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_usuarios_schema import JUsuarioCreate, JUsuarioUpdate, JUsuarioResponse
from app.services.j_usuarios_service import j_usuarios_service
from app.core.j_security import j_requiere_roles

j_usuarios_router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
    dependencies=[Depends(j_requiere_roles(["ADMIN"]))]
)


@j_usuarios_router.get(
    "",
    response_model=List[JUsuarioResponse],
    summary="Listar todos los usuarios (ADMIN)"
)
def j_listar_usuarios(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200)
):
    return j_usuarios_service.j_listar_usuarios(salto=salto, limite=limite)


@j_usuarios_router.get(
    "/{id}",
    response_model=JUsuarioResponse,
    summary="Obtener un usuario por ID (ADMIN)"
)
def j_obtener_usuario(id: str):
    return j_usuarios_service.j_obtener_por_id(id)


@j_usuarios_router.post(
    "",
    response_model=JUsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario con rol (ADMIN)"
)
def j_crear_usuario(datos: JUsuarioCreate):
    return j_usuarios_service.j_crear_usuario(datos)


@j_usuarios_router.put(
    "/{id}",
    response_model=JUsuarioResponse,
    summary="Actualizar información de un usuario (ADMIN)"
)
def j_actualizar_usuario(id: str, datos: JUsuarioUpdate):
    return j_usuarios_service.j_actualizar_usuario(id, datos)


@j_usuarios_router.delete(
    "/{id}",
    summary="Eliminar usuario (ADMIN - Aplica RN04 borrado lógico si tiene movimientos)"
)
def j_eliminar_usuario(id: str):
    return j_usuarios_service.j_eliminar_usuario(id)
