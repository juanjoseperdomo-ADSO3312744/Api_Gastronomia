# API REST Unidad Productiva de Gastronomía (CGDSS - SENA)

Sistema Backend REST completo y profesional desarrollado con **Python**, **FastAPI** y **MongoDB NoSQL**, diseñado para centralizar y gestionar los procesos operativos de la Unidad Productiva de Gastronomía del **Centro de Gestión y Desarrollo Sostenible Surcolombiano (CGDSS)**.

> **Programa:** Análisis y Desarrollo de Software (ADSO) — Ficha 3312744  
> **Aprendiz:** Juan José Perdomo Trejos (Nomenclatura con prefijo `j_`)  
> **Instructor Técnico:** Wilson Martínez  
> **Base de Datos Única:** MongoDB 7.0+ (NoSQL)

---

## 1. Características y Alcance del Proyecto

- **Base de Datos 100% NoSQL (MongoDB):** Todo el sistema opera sobre colecciones de documentos de MongoDB mediante PyMongo, sin dependencias de MySQL ni SQLAlchemy.
- **Autenticación y Seguridad:** Tokens Bearer JWT con tiempo de expiración y contraseñas cifradas mediante **bcrypt** (RN06).
- **Control de Acceso Basado en Roles (RBAC):** Restricciones granulares para roles `ADMIN`, `CAJERO` y `COCINERO`.
- **Arquitectura en Capas:**
  - `routers/`: Controladores de endpoints con prefijo `/api/v1` y documentación OpenAPI.
  - `services/`: Lógica de negocio y reglas del instructivo formativo (RN01 a RN06).
  - `repositories/`: Capa de persistencia y consultas hacia MongoDB.
  - `models/`: Enumeraciones y constantes del dominio gastronómico.
  - `schemas/`: Validación declarativa de datos de entrada y salida con Pydantic.
  - `core/`: Configuración global y utilidades criptográficas de seguridad.
  - `database/`: Conexión singleton a MongoDB y scripts DDL/DML.

---

## 2. Reglas de Negocio Implementadas

| Regla | Descripción | Estado de Cumplimiento |
|:---:|:---|:---:|
| **RN01** | El subtotal de cada ítem (`cantidad * precio_unitario`) y el total del pedido (`sum(subtotales)`) son calculados estrictamente por la API a partir del catálogo oficial, nunca por el cliente. | **100% Implementado** |
| **RN02** | Al registrar una compra, se incrementa automáticamente el `stock_actual` de cada insumo y se actualiza su `costo_unitario`. | **100% Implementado** |
| **RN03** | Al cambiar un pedido a estado `ENTREGADO`, la API calcula los insumos requeridos según las recetas de cada producto y descuenta el inventario. Si no hay existencias suficientes, responde con **HTTP 409 Conflict** y no modifica el stock. | **100% Implementado** |
| **RN04** | No se permite eliminar productos, insumos, clientes o proveedores con movimientos asociados; en su lugar, se realiza borrado lógico cambiando su estado a `INACTIVO`. | **100% Implementado** |
| **RN05** | Un pedido en estado `ENTREGADO` o `ANULADO` es inmutable: no permite modificaciones de ítems ni cambios de estado posteriores (retorna HTTP 400). | **100% Implementado** |
| **RN06** | Todas las contraseñas se almacenan cifradas con `bcrypt` y **nunca** se exponen en las respuestas de la API. | **100% Implementado** |

---

## 3. Matriz de Requerimientos Funcionales (RF01 - RF12)

| Código | Requerimiento | Endpoint(s) | Roles Autorizados |
|:---:|:---|:---|:---:|
| **RF01** | Autenticación y generación de tokens JWT | `POST /api/v1/auth/login`<br>`GET /api/v1/auth/perfil` | Público / Todos autenticados |
| **RF02** | Gestión de usuarios con roles | `CRUD /api/v1/usuarios`<br>`POST /api/v1/auth/registro` | ADMIN |
| **RF03** | Gestión de categorías de productos | `CRUD /api/v1/categorias` | ADMIN (Consulta: Todos) |
| **RF04** | Gestión de productos y precios de venta | `CRUD /api/v1/productos`<br>`GET /api/v1/productos/categoria/{id}` | ADMIN (Consulta: Todos) |
| **RF05** | Gestión de recetas (fichas técnicas) | `CRUD /api/v1/recetas`<br>`GET /api/v1/productos/{id}/receta` | ADMIN, COCINERO |
| **RF06** | Costo de producción y margen comercial | `GET /api/v1/productos/{id}/costo` | ADMIN, COCINERO |
| **RF07** | Control de insumos, stock bajo y vencimiento | `CRUD /api/v1/insumos`<br>`GET /api/v1/insumos/stock-bajo`<br>`GET /api/v1/insumos/por-vencer?dias=7` | ADMIN, COCINERO |
| **RF08** | Proveedores y registro de compras | `CRUD /api/v1/proveedores`<br>`CRUD /api/v1/compras`<br>`GET /api/v1/proveedores/{id}/compras` | ADMIN |
| **RF09** | Gestión de clientes por tipo (SENA y externos)| `CRUD /api/v1/clientes`<br>`GET /api/v1/clientes/{id}/pedidos` | ADMIN, CAJERO |
| **RF10** | Pedidos, comandas y cambio de estado | `CRUD /api/v1/pedidos`<br>`GET /api/v1/pedidos/estado/{estado}`<br>`PATCH /api/v1/pedidos/{id}/estado` | ADMIN, CAJERO (Cambio estado: COCINERO, ADMIN, CAJERO) |
| **RF11** | Reportes de ventas y más vendidos | `GET /api/v1/reportes/ventas`<br>`GET /api/v1/reportes/productos-mas-vendidos` | ADMIN |
| **RF12** | Calificaciones no estructuradas de clientes | `CRUD /api/v1/calificaciones`<br>`GET /api/v1/calificaciones/producto/{id}` | ADMIN, CAJERO |

---

## 4. Estructura del Proyecto

```
j_j_api_gastronomia/
├── app/
│   ├── main.py                     # Punto de entrada estándar ASGI para uvicorn
│   ├── j_main.py                   # Configuración de FastAPI, middlewares y rutas
│   ├── core/
│   │   ├── j_config.py             # Configuración Pydantic cargada de .env
│   │   └── j_security.py           # Bcrypt hashing, creación/validación de JWT y dependencias RBAC
│   ├── database/
│   │   └── j_conexion_mongo.py     # Cliente PyMongo singleton y utilidades ObjectId
│   ├── models/
│   │   └── j_models.py             # Enumeraciones (JRolUsuario, JEstadoPedido, etc.)
│   ├── schemas/                    # Modelos Pydantic para validación y serialización
│   │   ├── j_auth_schema.py
│   │   ├── j_usuarios_schema.py
│   │   ├── j_categorias_schema.py
│   │   ├── j_productos_schema.py
│   │   ├── j_insumos_schema.py
│   │   ├── j_recetas_schema.py
│   │   ├── j_proveedores_schema.py
│   │   ├── j_compras_schema.py
│   │   ├── j_clientes_schema.py
│   │   ├── j_pedidos_schema.py
│   │   ├── j_calificaciones_schema.py
│   │   └── j_reportes_schema.py
│   ├── repositories/               # Consultas y operaciones CRUD directas a MongoDB
│   │   ├── j_base_repository.py
│   │   ├── j_usuarios_repository.py
│   │   ├── j_categorias_repository.py
│   │   ├── j_productos_repository.py
│   │   ├── j_insumos_repository.py
│   │   ├── j_recetas_repository.py
│   │   ├── j_proveedores_repository.py
│   │   ├── j_compras_repository.py
│   │   ├── j_clientes_repository.py
│   │   ├── j_pedidos_repository.py
│   │   └── j_calificaciones_repository.py
│   ├── services/                   # Lógica de negocio (RN01, RN02, RN03, RN04, RN05)
│   │   ├── j_auth_service.py
│   │   ├── j_usuarios_service.py
│   │   ├── j_categorias_service.py
│   │   ├── j_productos_service.py
│   │   ├── j_insumos_service.py
│   │   ├── j_recetas_service.py
│   │   ├── j_proveedores_service.py
│   │   ├── j_compras_service.py
│   │   ├── j_clientes_service.py
│   │   ├── j_pedidos_service.py
│   │   ├── j_calificaciones_service.py
│   │   └── j_reportes_service.py
│   └── routers/                    # Endpoints por recurso bajo /api/v1
│       ├── j_auth_router.py
│       ├── j_usuarios_router.py
│       ├── j_categorias_router.py
│       ├── j_productos_router.py
│       ├── j_insumos_router.py
│       ├── j_recetas_router.py
│       ├── j_proveedores_router.py
│       ├── j_compras_router.py
│       ├── j_clientes_router.py
│       ├── j_pedidos_router.py
│       ├── j_calificaciones_router.py
│       └── j_reportes_router.py
├── database/
│   ├── 01_mongo_schema_validation.js # Validaciones de colecciones con $jsonSchema
│   ├── 02_mongo_indices.js           # Creación de índices únicos y de consulta
│   ├── 03_mongo_datos_prueba.js      # Datos iniciales (10 registros por colección)
│   └── 04_init_db.py                 # Script Python ejecutable para poblar la BD
├── docker-compose.yml                # Despliegue de MongoDB en contenedor
├── requirements.txt                  # Dependencias del proyecto
├── .env.example                      # Plantilla de variables de entorno
├── .env                              # Archivo local de configuración
├── test_api.py                       # Suite completa de pruebas automatizadas E2E
├── j_j_api_gastronomia.postman_collection.json # Colección de Postman con pruebas
├── MANUAL_CONFIGURACION_BASE_DATOS.md# Formato 6 SENA adaptado a MongoDB
└── README.md                         # Guía paso a paso del proyecto
```

---

## 5. Instrucciones de Instalación y Ejecución Paso a Paso

### Prerrequisitos
- Python 3.11 o superior instalado.
- Docker y Docker Desktop instalados (o MongoDB instalado localmente en el puerto 27017).

### Paso 1: Clonar o ubicarse en el directorio
```bash
cd "j_j_api_gastronomia"
```

### Paso 2: Crear y activar el entorno virtual (opcional pero recomendado)
```bash
# En Windows PowerShell / CMD:
python -m venv venv
venv\Scripts\activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno
Copiar el archivo de plantilla `.env.example` a `.env`:
```bash
# Windows PowerShell:
Copy-Item .env.example .env

# O verificar el contenido de .env existente:
cat .env
```
Contenido predeterminado:
```env
PROJECT_NAME="API REST Gastronomia CGDSS"
API_V1_STR="/api/v1"
ENVIRONMENT="development"
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=bd_gastronomia_nosql
SECRET_KEY=clave_secreta_super_segura_para_jwt_gastronomia_sena_2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

### Paso 5: Levantar MongoDB con Docker
```bash
docker compose up -d
```
Verificar que el contenedor `j_gastronomia_mongo` esté corriendo en el puerto `27017`:
```bash
docker ps
```

### Paso 6: Inicializar la base de datos con índices y datos de prueba
Ejecutar el script automatizado:
```bash
python database/04_init_db.py
```
Este script aplicará las validaciones, creará los índices únicos y sembrará al menos 10 registros por cada colección con contraseñas encriptadas.

### Paso 7: Iniciar el servidor de la API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
La API quedará disponible en:
- **Página de inicio:** [http://localhost:8000/](http://localhost:8000/)
- **Documentación Interactiva Swagger (OpenAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentación ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health check:** [http://localhost:8000/health](http://localhost:8000/health)

---

## 6. Credenciales de Prueba Precargadas

| Rol | Correo Electrónico | Contraseña | Alcance de Permisos |
|:---:|:---|:---:|:---|
| **ADMIN** | `admin@gastronomia.sena.edu.co` | `admin123` | Acceso total a todos los módulos y reportes. |
| **CAJERO** | `cajero1@gastronomia.sena.edu.co` | `cajero123` | Clientes, pedidos, comanda, calificaciones y consulta de menú. |
| **COCINERO** | `cocinero1@gastronomia.sena.edu.co` | `cocinero123` | Insumos, stock bajo, vencimiento, recetas, costos y cambio de estado de pedidos. |

---

## 7. Ejecución de Pruebas Automatizadas

El proyecto incluye una suite de pruebas de integración E2E en `test_api.py`. Para ejecutarla:
```bash
python test_api.py
```
La suite valida automáticamente:
1. Endpoints generales (`/`, `/health`).
2. Autenticación y rechazo 401 ante credenciales incorrectas.
3. Permisos RBAC y respuesta 403 Forbidden para accesos no autorizados.
4. Regla RN06: Ninguna respuesta incluye contraseñas ni hashes.
5. Catálogo, categorías y cálculo de costo y margen de ganancia (RF06).
6. Regla RN02: Compras incrementan stock y actualizan costo unitario.
7. Regla RN01: Subtotal y total calculados por la API.
8. Regla RN03: Descuento de stock al entregar y respuesta HTTP 409 Conflict si no hay inventario suficiente.
9. Regla RN05: Inmutabilidad de pedidos entregados ante ediciones (HTTP 400).
10. Regla RN04: Borrado lógico a INACTIVO si hay movimientos asociados.
11. Calificaciones no estructuradas en MongoDB y promedios por producto (RF12).
12. Reporte de ventas y ranking de productos más vendidos (RF11).

---

## 8. Colección de Postman

Se incluye el archivo `j_j_api_gastronomia.postman_collection.json`.

### Cómo probar en Postman:
1. Abrir Postman y hacer clic en **Import**.
2. Seleccionar el archivo `j_j_api_gastronomia.postman_collection.json`.
3. Ejecutar la petición `01. Autenticación / Login - ADMIN`. El script de prueba guardará automáticamente el token JWT en las variables de la colección (`{{token_admin}}`).
4. Probar los demás endpoints: todos heredan la autenticación y las variables de prueba dinámicamente.

---

## 9. Anexo: Manual de Configuración de Base de Datos

Consulte el documento independiente [MANUAL_CONFIGURACION_BASE_DATOS.md](MANUAL_CONFIGURACION_BASE_DATOS.md) para revisar el diligenciamiento completo del **Formato 6 SENA** adaptado a MongoDB, incluyendo el diccionario de datos detallado, el modelo documental Mermaid, la justificación de motores y los procedimientos de respaldo (`mongodump` y `mongorestore`).
