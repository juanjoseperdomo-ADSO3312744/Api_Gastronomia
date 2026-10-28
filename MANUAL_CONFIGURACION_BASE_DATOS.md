# FORMATO 6: MANUAL DE CONFIGURACIÓN DE BASE DE DATOS
## UNIDAD PRODUCTIVA DE GASTRONOMÍA — CGDSS SENA
### PROYECTO: API REST CON PYTHON, FASTAPI Y MONGODB NoSQL

---

## 1. HISTORIAL DE REVISIÓN Y CAMBIOS

| Versión | Fecha | Responsable de Elaboración | Responsable de Revisión | Responsable de Aprobación | Descripción del Cambio |
|:---:|:---:|:---|:---|:---|:---|
| **1.0.0** | 2026-10-21 | **Juan José Perdomo Trejos**<br>(Aprendiz ADSO) | **Wilson Martínez**<br>(Instructor Técnico SENA) | **Líder Unidad Productiva**<br>(Gastronomía CGDSS) | Versión inicial del manual de base de datos adaptado 100% al modelo documental NoSQL de MongoDB para la Unidad Productiva de Gastronomía. |

---

## 2. INTRODUCCIÓN

El presente documento constituye el **Manual de Configuración de Base de Datos** para el sistema de información de la **Unidad Productiva de Gastronomía** del **Centro de Gestión y Desarrollo Sostenible Surcolombiano (CGDSS) - SENA**. 

El propósito central de esta base de datos es proporcionar almacenamiento persistente, centralizado, consistente, seguro y de alto rendimiento para soportar las operaciones de la API REST desarrollada en FastAPI. Permite digitalizar y automatizar los flujos críticos de la unidad: control estricto de existencias e inventario de insumos, estandarización de recetas (fichas técnicas), cálculo de costos de producción y márgenes comerciales de venta, registro centralizado de compras a proveedores, control de clientes institucionales (aprendices, instructores, funcionarios) y externos, ciclo de vida de los pedidos (desde pendiente hasta entregado o anulado) y recopilación no estructurada de opiniones y calificaciones de servicio de los clientes.

---

## 3. ALCANCE

### 3.1 Procesos Cubiertos en el Prototipo
1. **Seguridad y Control de Acceso:** Gestión de usuarios, autenticación mediante JWT y autorización granular basada en roles (`ADMIN`, `CAJERO`, `COCINERO`).
2. **Catálogo de Productos y Categorías:** Clasificación taxonómica de productos elaborados y comercializados.
3. **Fichas Técnicas (Recetas):** Mapeo de insumos requeridos por unidad de producto terminado.
4. **Costeo y Rentabilidad:** Determinación automática del costo de producción según los insumos y evaluación del margen bruto de ganancia.
5. **Inventario de Insumos:** Monitoreo de existencias en tiempo real, alertas de stock mínimo y control de fechas de vencimiento.
6. **Compras a Proveedores:** Entrada formal de insumos, actualización automática de inventarios y registro de costos unitarios de adquisición (RN02).
7. **Gestión de Clientes:** Clasificación por tipo (`APRENDIZ`, `INSTRUCTOR`, `FUNCIONARIO`, `EXTERNO`) y seguimiento de su historial de compras.
8. **Gestión de Pedidos y Ventas:** Registro de pedidos con cálculo automático de subtotales y totales (RN01), control transaccional del stock al entregar (RN03) e inmutabilidad de pedidos terminados (RN05).
9. **Calificaciones y Retroalimentación:** Almacenamiento no estructurado en formato BSON/JSON de encuestas de servicio y valoración de productos (RF12).
10. **Reportes e Inteligencia de Negocio:** Informes de ventas por rango de fechas y ranking de los productos más vendidos mediante pipelines de agregación.

### 3.2 Elementos Fuera del Prototipo
- Integración con pasarelas de pago bancario en línea (PSE, tarjetas de crédito externas).
- Facturación electrónica DIAN (se maneja numeración de facturas internas del proveedor).
- Gestión de nómina o turnos laborales del personal de cocina.
- Módulos de logística y transporte de domicilios externos.

---

## 4. RESPONSABLES E INVOLUCRADOS

| Nombre Completo | Rol en el Proyecto | Dependencia / Entidad | Correo Electrónico |
|:---|:---:|:---:|:---|
| **Juan José Perdomo Trejos** | Desarrollador Backend / DBA (Responsable) | Aprendiz ADSO Ficha 3312744 - SENA CGDSS | jperdomo@gastronomia.sena.edu.co |
| **Wilson Martínez** | Instructor Técnico (Revisor) | Centro de Gestión y Desarrollo Sostenible Surcolombiano | wmartinez@sena.edu.co |
| **Líder de Unidad Productiva** | Interesado Principal / Product Owner (Aprobador) | Unidad Productiva de Gastronomía CGDSS | gastronomia.cgdss@sena.edu.co |

---

## 5. MODELO ENTIDAD-RELACIÓN / DOCUMENTAL (MER)

El modelo de datos fue adaptado de forma óptima a la arquitectura de documentos de MongoDB (`bd_gastronomia_nosql`). Combina **referencias directas por ObjectId/String** para entidades con ciclo de vida independiente y **documentos anidados (Embedded Documents)** para detalles transaccionales (como los ítems de compra, productos de un pedido y valoraciones por ítem en calificaciones).

```mermaid
erDiagram
    USUARIOS {
        ObjectId _id PK
        string identificacion UQ
        string nombres
        string apellidos
        string correo UQ
        string password "bcrypt hash"
        string rol "ADMIN|CAJERO|COCINERO"
        string estado "ACTIVO|INACTIVO"
    }

    CATEGORIAS {
        ObjectId _id PK
        string nombre UQ
        string descripcion
        string estado "ACTIVO|INACTIVO"
    }

    PRODUCTOS {
        ObjectId _id PK
        string codigo UQ
        string nombre
        string descripcion
        double precio_venta "gt 0"
        string unidad_venta
        string id_categoria FK
        string estado "DISPONIBLE|AGOTADO|INACTIVO"
    }

    INSUMOS {
        ObjectId _id PK
        string nombre UQ
        string unidad_medida "g|kg|ml|l|lb|unidad"
        double stock_actual "ge 0"
        double stock_minimo "ge 0"
        double costo_unitario "ge 0"
        string fecha_vencimiento
        string estado "ACTIVO|INACTIVO"
    }

    RECETAS {
        ObjectId _id PK
        string id_producto FK
        string id_insumo FK
        double cantidad "gt 0"
    }

    PROVEEDORES {
        ObjectId _id PK
        string nit UQ
        string razon_social
        string telefono
        string correo
        string direccion
        string estado "ACTIVO|INACTIVO"
    }

    COMPRAS {
        ObjectId _id PK
        string numero_factura UQ
        string fecha_compra
        string id_proveedor FK
        string id_usuario FK
        double total
        array detalle "Embedded items"
    }

    CLIENTES {
        ObjectId _id PK
        string identificacion UQ
        string nombres
        string apellidos
        string telefono
        string correo
        string tipo_cliente "APRENDIZ|INSTRUCTOR|FUNCIONARIO|EXTERNO"
        string estado "ACTIVO|INACTIVO"
    }

    PEDIDOS {
        ObjectId _id PK
        string fecha_pedido
        string id_cliente FK
        string id_usuario FK
        string tipo_pedido "MESA|PARA_LLEVAR|EVENTO"
        string estado "PENDIENTE|EN_PREPARACION|ENTREGADO|ANULADO"
        double total
        string observaciones
        array detalle "Embedded items"
    }

    CALIFICACIONES {
        ObjectId _id PK
        string id_pedido FK
        string id_cliente FK
        string fecha
        int calificacion_servicio "1 a 5"
        string comentario
        array productos "Embedded items"
    }

    CATEGORIAS ||--o{ PRODUCTOS : "agrupa (1:N)"
    PRODUCTOS ||--o{ RECETAS : "se compone de (1:N)"
    INSUMOS ||--o{ RECETAS : "es insumo de (1:N)"
    PROVEEDORES ||--o{ COMPRAS : "suministra (1:N)"
    USUARIOS ||--o{ COMPRAS : "registra (1:N)"
    CLIENTES ||--o{ PEDIDOS : "solicita (1:N)"
    USUARIOS ||--o{ PEDIDOS : "atiende (1:N)"
    PEDIDOS ||--o| CALIFICACIONES : "evaluado en (1:1)"
    CLIENTES ||--o{ CALIFICACIONES : "emite (1:N)"
```

---

## 6. DICCIONARIO DE DATOS (COLECCIONES MONGODB)

### 6.1 Colección: `usuarios`
Almacena las credenciales y roles del personal del sistema.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único por documento | Identificador primario en MongoDB |
| `identificacion` | String | 3-20 caracteres | No | UQ | - | Índice único | Cédula o tarjeta de identidad |
| `nombres` | String | 2-80 caracteres | No | No | - | Min 2 letras | Nombres del empleado/aprendiz |
| `apellidos` | String | 2-80 caracteres | No | No | - | Min 2 letras | Apellidos del usuario |
| `correo` | String | 5-120 caracteres | No | UQ | - | Patrón email + Índice único | Correo electrónico de inicio de sesión |
| `password` | String | 60 caracteres | No | No | - | Bcrypt Hash (RN06) | Hash seguro de la contraseña |
| `rol` | String | Enum | No | No | - | ADMIN, CAJERO, COCINERO | Rol asignado para permisos RBAC |
| `estado` | String | Enum | No | No | "ACTIVO" | ACTIVO, INACTIVO | Estado de la cuenta de acceso |

### 6.2 Colección: `categorias`
Clasificación de los productos gastronómicos ofrecidos.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único por documento | Identificador de categoría |
| `nombre` | String | 2-60 caracteres | No | UQ | - | Índice único insensible a mayúsculas | Nombre de la categoría (Platos, Bebidas...) |
| `descripcion` | String | Max 200 caracteres | Sí | No | "" | Texto descriptivo | Detalle del alcance de la categoría |
| `estado` | String | Enum | No | No | "ACTIVO" | ACTIVO, INACTIVO | Estado para borrado lógico |

### 6.3 Colección: `productos`
Artículos terminados destinados a la venta.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único | Identificador del producto |
| `codigo` | String | 2-20 caracteres | No | UQ | - | Índice único en mayúsculas | Código interno (ej: PRD-001) |
| `nombre` | String | 2-100 caracteres | No | No | - | Min 2 caracteres | Nombre comercial del plato o bebida |
| `descripcion` | String | Texto libre | Sí | No | "" | - | Descripción comercial e ingredientes |
| `precio_venta` | Double | Decimal(10,2) | No | No | - | > 0 | Precio final al público |
| `unidad_venta` | String | Max 20 caracteres | No | No | - | Porción, vaso, plato, unidad... | Unidad de expendio comercial |
| `id_categoria` | String | 24 hex | No | FK | - | Referencia a `categorias._id` | Categoría a la que pertenece |
| `estado` | String | Enum | No | No | "DISPONIBLE" | DISPONIBLE, AGOTADO, INACTIVO | Estado operativo del producto |

### 6.4 Colección: `insumos`
Materias primas e insumos controlados en almacén y cocina.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único | Identificador del insumo |
| `nombre` | String | 2-100 caracteres | No | UQ | - | Índice único | Nombre de la materia prima |
| `unidad_medida`| String | Enum | No | No | - | g, kg, ml, l, lb, unidad | Unidad estandarizada de medida |
| `stock_actual` | Double | Decimal(10,2) | No | No | 0.0 | >= 0 | Existencias físicas en bodega |
| `stock_minimo` | Double | Decimal(10,2) | No | No | 0.0 | >= 0 | Umbral mínimo para alertas de stock |
| `costo_unitario`| Double | Decimal(10,2) | No | No | 0.0 | >= 0 (RN02) | Costo de adquisición por unidad |
| `fecha_vencimiento`| String/Date | YYYY-MM-DD | Sí | No | null | Fecha válida | Vencimiento del lote actual en inventario |
| `estado` | String | Enum | No | No | "ACTIVO" | ACTIVO, INACTIVO | Estado del insumo (RN04) |

### 6.5 Colección: `recetas`
Fichas técnicas que especifican el consumo de insumos por cada producto.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único | Identificador del ítem de receta |
| `id_producto` | String | 24 hex | No | FK | - | Referencia a `productos._id` | Producto que se elabora |
| `id_insumo` | String | 24 hex | No | FK | - | Referencia a `insumos._id` | Insumo que compone la receta |
| `cantidad` | Double | Decimal(10,3) | No | No | - | > 0 | Cantidad requerida de insumo |

### 6.6 Colección: `proveedores`
Empresas y distribuidoras que abastecen la unidad productiva.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único | Identificador del proveedor |
| `nit` | String | 3-20 caracteres | No | UQ | - | Índice único | NIT o cédula del proveedor |
| `razon_social` | String | 2-120 caracteres | No | No | - | - | Nombre o razón social comercial |
| `telefono` | String | Max 30 caracteres | Sí | No | "" | - | Teléfono de contacto |
| `correo` | String | Max 120 caracteres | Sí | No | null | Correo electrónico | Correo para pedidos y cotizaciones |
| `direccion` | String | Max 150 caracteres | Sí | No | "" | - | Dirección física de despacho |
| `estado` | String | Enum | No | No | "ACTIVO" | ACTIVO, INACTIVO | Estado operativo (RN04) |

### 6.7 Colección: `compras`
Facturas y recibos de adquisición de insumos a proveedores.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único | Identificador de la compra |
| `numero_factura`| String | 1-30 caracteres | No | UQ | - | Índice único | Factura expedida por el proveedor |
| `fecha_compra` | String/Date | ISO 8601 | No | No | Ahora | Formato timestamp | Fecha y hora de recepción |
| `id_proveedor` | String | 24 hex | No | FK | - | Referencia a `proveedores._id` | Proveedor seleccionado |
| `id_usuario` | String | 24 hex | No | FK | - | Referencia a `usuarios._id` | Empleado que registró la compra |
| `total` | Double | Decimal(12,2) | No | No | - | Suma de subtotales | Total neto de la factura |
| `detalle` | Array | Lista de objetos | No | No | - | Min 1 elemento | Ítems comprados (insumo, cantidad, costo, subtotal) |

### 6.8 Colección: `clientes`
Comunidad SENA y clientes externos que realizan pedidos.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único | Identificador del cliente |
| `identificacion`| String | 3-20 caracteres | No | UQ | - | Índice único | Cédula o documento de identidad |
| `nombres` | String | 2-80 caracteres | No | No | - | Min 2 letras | Nombres del cliente |
| `apellidos` | String | 2-80 caracteres | No | No | - | Min 2 letras | Apellidos del cliente |
| `telefono` | String | Max 30 caracteres | Sí | No | "" | - | Teléfono móvil |
| `correo` | String | Max 120 caracteres | Sí | No | null | Correo electrónico | Correo institucional o personal |
| `tipo_cliente` | String | Enum | No | No | - | APRENDIZ, INSTRUCTOR, FUNCIONARIO, EXTERNO | Segmento de cliente institucional |
| `estado` | String | Enum | No | No | "ACTIVO" | ACTIVO, INACTIVO | Estado del cliente (RN04) |

### 6.9 Colección: `pedidos`
Órdenes de servicio y ventas realizadas.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único | Identificador del pedido |
| `fecha_pedido` | String/Date | ISO 8601 | No | No | Ahora | - | Fecha y hora en que se toma la comanda |
| `id_cliente` | String | 24 hex | No | FK | - | Referencia a `clientes._id` | Cliente que realiza el pedido |
| `id_usuario` | String | 24 hex | No | FK | - | Referencia a `usuarios._id` | Cajero/usuario que ingresa el pedido |
| `tipo_pedido` | String | Enum | No | No | - | MESA, PARA_LLEVAR, EVENTO | Modalidad de servicio |
| `estado` | String | Enum | No | No | "PENDIENTE" | PENDIENTE, EN_PREPARACION, ENTREGADO, ANULADO | Estado del flujo del pedido (RN03, RN05) |
| `total` | Double | Decimal(12,2) | No | No | - | Calculado en backend (RN01) | Monto total a cobrar |
| `observaciones`| String | Texto libre | Sí | No | "" | - | Notas de preparación o mesa |
| `detalle` | Array | Lista de objetos | No | No | - | Min 1 elemento | Ítems pedidos (producto, cantidad, precio, subtotal) |

### 6.10 Colección: `calificaciones` (Colección NoSQL no estructurada)
Evaluaciones y opiniones emitidas por los comensales sobre su experiencia gastronómica.
| Campo | Tipo BSON | Tamaño / Formato | Nulo | Llave | Valor Defecto | Restricción / Validación | Descripción |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `_id` | ObjectId | 12 bytes (24 hex) | No | PK | Auto-generado | Único | Identificador de la evaluación |
| `id_pedido` | String | 24 hex | No | FK | - | Referencia a `pedidos._id` | Pedido sobre el cual opina |
| `id_cliente` | String | 24 hex | No | FK | - | Referencia a `clientes._id` | Cliente que califica |
| `fecha` | String/Date | ISO 8601 | No | No | Ahora | - | Momento de la calificación |
| `calificacion_servicio` | Int | Entero 1 a 5 | No | No | - | Entre 1 y 5 estrellas | Evaluación general del servicio recibido |
| `comentario` | String | Texto libre | Sí | No | "" | - | Texto de opinión o sugerencia del cliente |
| `productos` | Array | Lista de objetos | No | No | [] | Array embebido | Calificación individual por producto consumido |

---

## 7. JUSTIFICACIÓN DEL MOTOR SELECCIONADO (MONGODB vs RELACIONALES)

| Criterio | MongoDB 7.0 / 8.0 (Seleccionado) | MySQL 8.0 | PostgreSQL 16 | SQL Server / Oracle |
|:---|:---|:---|:---|:---|
| **Paradigma de Almacenamiento** | **Documental NoSQL (BSON/JSON)**. Estructuras anidadas naturales. | Tabular Relacional rígido (Filas y Columnas). | Objeto-Relacional con soporte parcial JSONB. | Relacional empresarial tradicional con alto costo de licenciamiento. |
| **Manejo de Detalles y Subdocumentos** | **Excelente**. Permite anidar los detalles de pedidos, compras y valoraciones en una sola lectura sin JOINs costosos. | Requiere tablas intermedias normalizadas y JOINs múltiples. | Requiere extensiones o esquemas mixtos normalizados. | Altamente complejo y restrictivo para esquemas dinámicos. |
| **Calificaciones y Datos No Estructurados** | **Nativo**. Ideal para encuestas dinámicas, opiniones con cantidad variable de ítems calificados y cambios futuros en formularios. | Ineficiente para encuestas dinámicas sin esquemas EAV engorrosos. | Aceptable mediante JSONB pero con sintaxis compleja. | Rígido, requiere tablas adicionales para cada atributo nuevo. |
| **Flexibilidad y Adaptabilidad** | **Alta**. Validación declarativa mediante `$jsonSchema`, permitiendo evolución ágil de versiones de API. | Migraciones DDL lentas con bloqueo de tablas (`ALTER TABLE`). | Migraciones robustas pero complejas. | Proceso burocrático y costoso en entornos empresariales. |
| **Consumo por API REST (FastAPI)** | **Integración 100% natural**. Los documentos BSON se serializan y parsean directamente a esquemas Pydantic. | Requiere mapeo relacional (ORM) con sobrecarga de conversión. | Requiere ORM (SQLAlchemy) o adaptadores relacionales. | Requiere drivers ODBC/JDBC pesados. |
| **Costo y Despliegue** | **Open Source / Gratuito** con soporte oficial para contenedores Docker livianos. | Open Source / GPL. | Open Source libre. | Licenciamiento comercial muy costoso por núcleo de CPU. |

**Conclusión Técnica:**  
El uso de **MongoDB como base de datos única** simplifica drásticamente la arquitectura del software al eliminar la sobrecarga de mantener dos motores heterogéneos (MySQL + MongoDB). Ofrece alta velocidad de lectura y escritura en comanda digital, permite almacenar de forma atómica pedidos y compras con sus detalles en un solo documento, y otorga versatilidad plena para las calificaciones y reportes estadísticos.

---

## 8. REQUISITOS DE CONFIGURACIÓN

1. **Entorno de Contenedores:**
   - Docker Desktop / Docker Engine versión 24+
   - Imagen oficial de MongoDB: `mongo:7.0` o `mongo:latest`
2. **Entorno de Programación:**
   - Python 3.11 o superior (instalado 3.12.10 en el entorno de desarrollo)
   - Librerías principales: `fastapi`, `uvicorn[standard]`, `pymongo`, `pydantic`, `pydantic-settings`, `python-jose`, `bcrypt`, `python-dotenv`, `httpx`
3. **Clientes de Administración:**
   - MongoDB Compass (GUI gráfica oficial) o Studio 3T
   - MongoDB Shell (`mongosh`) desde terminal o contenedor
4. **Parámetros del Sistema:**
   - Puerto de escucha por defecto: `27017`
   - Zona horaria de operaciones: `America/Bogota` (UTC-5)
   - Charset y codificación: `UTF-8`

---

## 9. CONFIGURACIÓN Y EJECUCIÓN PASO A PASO

### Paso 1: Levantar MongoDB mediante Docker
Ejecutar en la carpeta `j_j_api_gastronomia`:
```bash
docker compose up -d
```
Verificar que el contenedor `j_gastronomia_mongo` esté activo:
```bash
docker ps
```

### Paso 2: Ejecutar los Scripts de Inicialización e Índices
Mediante el script automatizado en Python:
```bash
python database/04_init_db.py
```
O directamente desde `mongosh`:
```bash
mongosh "mongodb://localhost:27017/bd_gastronomia_nosql" database/01_mongo_schema_validation.js
mongosh "mongodb://localhost:27017/bd_gastronomia_nosql" database/02_mongo_indices.js
mongosh "mongodb://localhost:27017/bd_gastronomia_nosql" database/03_mongo_datos_prueba.js
```

### Paso 3: Evidencias de Creación y Consultas
Comprobar en la consola de MongoDB:
```javascript
// Mostrar colecciones creadas
show collections;

// Contar documentos
db.usuarios.countDocuments();
db.productos.countDocuments();
db.pedidos.countDocuments();

// Inspeccionar índices
db.usuarios.getIndexes();
db.productos.getIndexes();
```

---

## 10. OTRAS CONSIDERACIONES TÉCNICAS

### 10.1 Procedimiento de Respaldo (Backup)
Para generar un dump binario completo de la base de datos:
```bash
docker exec -t j_gastronomia_mongo mongodump --db bd_gastronomia_nosql --out /data/db/backup_$(date +%Y%m%d)
```
O desde la máquina anfitriona con herramientas de MongoDB:
```bash
mongodump --uri="mongodb://localhost:27017/bd_gastronomia_nosql" --out="./backups"
```

### 10.2 Procedimiento de Restauración (Restore)
Para restaurar una copia de seguridad previamente generada:
```bash
mongorestore --uri="mongodb://localhost:27017" --drop ./backups/bd_gastronomia_nosql
```

### 10.3 Manejo Seguro de Credenciales
- Todas las cadenas de conexión (`MONGO_URI`, `MONGO_DB_NAME`) y la clave de firma de tokens (`SECRET_KEY`) se administran mediante archivos de entorno `.env`.
- El archivo `.env` se encuentra ignorado en el control de versiones para evitar filtraciones de seguridad.
- En producción, MongoDB debe configurarse con autenticación por usuario y contraseña (`authSource=admin`) con privilegios mínimos asignados a la base de datos `bd_gastronomia_nosql` mediante el comando `db.createUser()`.
