from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.j_reportes_schema import (
    JReporteVentasResponse,
    JReporteProductosMasVendidosResponse
)
from app.services.j_reportes_service import j_reportes_service
from app.core.j_security import j_requiere_roles

j_reportes_router = APIRouter(
    prefix="/reportes",
    tags=["Reportes y Estadísticas"],
    dependencies=[Depends(j_requiere_roles(["ADMIN"]))]
)


@j_reportes_router.get(
    "/ventas",
    response_model=JReporteVentasResponse,
    summary="Reporte de ventas totales por rango de fechas (Solo ADMIN - RF11)",
    description="Calcula el valor total vendido, número de pedidos y ticket promedio en un rango de fechas. Excluye pedidos anulados."
)
def j_reporte_ventas(
    desde: Optional[str] = Query(None, description="Fecha inicial en formato YYYY-MM-DD"),
    hasta: Optional[str] = Query(None, description="Fecha final en formato YYYY-MM-DD")
):
    return j_reportes_service.j_reporte_ventas(desde=desde, hasta=hasta)


@j_reportes_router.get(
    "/productos-mas-vendidos",
    response_model=JReporteProductosMasVendidosResponse,
    summary="Ranking de productos más vendidos (Solo ADMIN - RF11)",
    description="Genera el ranking de productos ordenados por unidades vendidas y recaudación utilizando agregaciones de MongoDB."
)
def j_reporte_productos_mas_vendidos(
    limite: int = Query(10, ge=1, le=100, description="Cantidad máxima de productos a incluir en el ranking")
):
    return j_reportes_service.j_productos_mas_vendidos(limite=limite)
