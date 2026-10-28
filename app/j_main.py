from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.j_config import j_settings
from app.database.j_conexion_mongo import JMongoConnection, j_obtener_bd
from app.routers.j_auth_router import j_auth_router
from app.routers.j_usuarios_router import j_usuarios_router
from app.routers.j_categorias_router import j_categorias_router
from app.routers.j_productos_router import j_productos_router
from app.routers.j_insumos_router import j_insumos_router
from app.routers.j_recetas_router import j_recetas_router
from app.routers.j_proveedores_router import j_proveedores_router
from app.routers.j_compras_router import j_compras_router
from app.routers.j_clientes_router import j_clientes_router
from app.routers.j_pedidos_router import j_pedidos_router
from app.routers.j_calificaciones_router import j_calificaciones_router
from app.routers.j_reportes_router import j_reportes_router


@asynccontextmanager
async def j_lifespan(app: FastAPI):
    # Inicialización de la conexión a MongoDB al arrancar
    try:
        cliente = JMongoConnection.j_conectar()
        cliente.admin.command("ping")
        print(f" Conexión exitosa a MongoDB en {j_settings.MONGO_URI}")
    except Exception as e:
        print(f" Advertencia: No se pudo conectar a MongoDB al iniciar: {e}")
    yield
    # Cierre de conexiones al apagar la aplicación
    JMongoConnection.j_cerrar()
    print(" Conexión a MongoDB cerrada.")


j_app = FastAPI(
    title=j_settings.PROJECT_NAME,
    description=(
        "API REST para la Unidad Productiva de Gastronomía del Centro de Gestión "
        "y Desarrollo Sostenible Surcolombiano (CGDSS - SENA). "
        "Desarrollada con Python, FastAPI y MongoDB NoSQL como base de datos única. "
        "Incluye autenticación JWT, RBAC por roles (ADMIN, CAJERO, COCINERO), "
        "gestión de recetas, control de stock, compras, pedidos y reglas de negocio RN01..RN06."
    ),
    version="1.0.0",
    lifespan=j_lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{j_settings.API_V1_STR}/openapi.json"
)

# Configuración de CORS para clientes web y móviles
j_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers con prefijo /api/v1
prefix = j_settings.API_V1_STR
j_app.include_router(j_auth_router, prefix=prefix)
j_app.include_router(j_usuarios_router, prefix=prefix)
j_app.include_router(j_categorias_router, prefix=prefix)
j_app.include_router(j_productos_router, prefix=prefix)
j_app.include_router(j_insumos_router, prefix=prefix)
j_app.include_router(j_recetas_router, prefix=prefix)
j_app.include_router(j_proveedores_router, prefix=prefix)
j_app.include_router(j_compras_router, prefix=prefix)
j_app.include_router(j_clientes_router, prefix=prefix)
j_app.include_router(j_pedidos_router, prefix=prefix)
j_app.include_router(j_calificaciones_router, prefix=prefix)
j_app.include_router(j_reportes_router, prefix=prefix)


@j_app.get("/", tags=["General"], summary="Ruta raíz de bienvenida")
def j_raiz():
    return {
        "mensaje": "Bienvenido a la API REST de la Unidad Productiva de Gastronomía (CGDSS - SENA)",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "estado_base_datos": "MongoDB NoSQL conectado",
        "prefijo_api": j_settings.API_V1_STR
    }


@j_app.get("/health", tags=["General"], summary="Verificación de estado de salud del servicio")
def j_health():
    try:
        cliente = JMongoConnection.j_conectar()
        cliente.admin.command("ping")
        bd_ok = True
    except Exception:
        bd_ok = False

    return {
        "status": "healthy" if bd_ok else "degraded",
        "mongodb_conectado": bd_ok,
        "base_datos": j_settings.MONGO_DB_NAME
    }
