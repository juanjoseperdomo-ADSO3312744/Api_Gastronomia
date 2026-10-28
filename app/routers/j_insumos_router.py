from typing import List
from fastapi import APIRouter, Depends, status, Query
from app.schemas.j_insumos_schema import JInsumoCreate, JInsumoUpdate, JInsumoResponse
from app.services.j_insumos_service import j_insumos_service
from app.core.j_security import j_requiere_roles

j_insumos_router = APIRouter(
    prefix="/insumos",
    tags=["Insumos"],
    dependencies=[Depends(j_requiere_roles(["ADMIN", "COCINERO"]))]
)


@j_insumos_router.get(
    "/stock-bajo",
    response_model=List[JInsumoResponse],
    summary="Consultar insumos con stock crítico o bajo (stock_actual <= stock_minimo) (RF07)"
)
def j_insumos_stock_bajo():
    return j_insumos_service.j_obtener_stock_bajo()


@j_insumos_router.get(
    "/por-vencer",
    response_model=List[JInsumoResponse],
    summary="Consultar insumos próximos a vencer en N días (RF07)"
)
def j_insumos_por_vencer(dias: int = Query(7, ge=1, le=365)):
    return j_insumos_service.j_obtener_por_vencer(dias=dias)


@j_insumos_router.get(
    "",
    response_model=List[JInsumoResponse],
    summary="Listar todos los insumos de inventario"
)
def j_listar_insumos(
    salto: int = Query(0, ge=0),
    limite: int = Query(100, ge=1, le=200)
):
    return j_insumos_service.j_listar_insumos(salto=salto, limite=limite)


@j_insumos_router.get(
    "/{id}",
    response_model=JInsumoResponse,
    summary="Obtener un insumo por ID"
)
def j_obtener_insumo(id: str):
    return j_insumos_service.j_obtener_por_id(id)


@j_insumos_router.post(
    "",
    response_model=JInsumoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo insumo"
)
def j_crear_insumo(datos: JInsumoCreate):
    return j_insumos_service.j_crear_insumo(datos)


@j_insumos_router.put(
    "/{id}",
    response_model=JInsumoResponse,
    summary="Actualizar información de un insumo"
)
def j_actualizar_insumo(id: str, datos: JInsumoUpdate):
    return j_insumos_service.j_actualizar_insumo(id, datos)


@j_insumos_router.delete(
    "/{id}",
    summary="Eliminar insumo (Aplica RN04 borrado lógico si tiene recetas o compras)"
)
def j_eliminar_insumo(id: str):
    return j_insumos_service.j_eliminar_insumo(id)
