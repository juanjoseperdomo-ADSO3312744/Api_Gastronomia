/**
 * Script 01: Creación de Colecciones y Esquemas de Validación ($jsonSchema) en MongoDB
 * Base de Datos: bd_gastronomia_nosql
 * Unidad Productiva de Gastronomía - CGDSS SENA
 */

const dbName = "bd_gastronomia_nosql";
const dbInstance = db.getSiblingDB(dbName);

print("Iniciando creación de colecciones con $jsonSchema en: " + dbName);

// 1. Colección: usuarios
dbInstance.createCollection("usuarios", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["identificacion", "nombres", "apellidos", "correo", "password", "rol", "estado"],
      properties: {
        identificacion: { bsonType: "string", description: "Documento de identidad único" },
        nombres: { bsonType: "string", description: "Nombres del usuario" },
        apellidos: { bsonType: "string", description: "Apellidos del usuario" },
        correo: { bsonType: "string", pattern: "^.+@.+\\..+$", description: "Correo electrónico único de acceso" },
        password: { bsonType: "string", description: "Hash seguro de la contraseña (bcrypt)" },
        rol: { enum: ["ADMIN", "CAJERO", "COCINERO"], description: "Rol de acceso del usuario" },
        estado: { enum: ["ACTIVO", "INACTIVO"], description: "Estado de la cuenta" }
      }
    }
  }
});

// 2. Colección: categorias
dbInstance.createCollection("categorias", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "estado"],
      properties: {
        nombre: { bsonType: "string", description: "Nombre de la categoría (Platos, Bebidas, etc.)" },
        descripcion: { bsonType: "string", description: "Descripción de la categoría" },
        estado: { enum: ["ACTIVO", "INACTIVO"], description: "Estado de la categoría" }
      }
    }
  }
});

// 3. Colección: productos
dbInstance.createCollection("productos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["codigo", "nombre", "precio_venta", "unidad_venta", "id_categoria", "estado"],
      properties: {
        codigo: { bsonType: "string", description: "Código interno único" },
        nombre: { bsonType: "string", description: "Nombre comercial del producto" },
        descripcion: { bsonType: "string" },
        precio_venta: { bsonType: ["double", "int", "decimal"], minimum: 0.01, description: "Precio de venta mayor a 0" },
        unidad_venta: { bsonType: "string", description: "Porción, vaso, plato, unidad..." },
        id_categoria: { bsonType: ["string", "objectId"], description: "Referencia a categorias" },
        estado: { enum: ["DISPONIBLE", "AGOTADO", "INACTIVO"], description: "Estado del producto" }
      }
    }
  }
});

// 4. Colección: insumos
dbInstance.createCollection("insumos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nombre", "unidad_medida", "stock_actual", "stock_minimo", "costo_unitario", "estado"],
      properties: {
        nombre: { bsonType: "string", description: "Nombre del insumo o materia prima" },
        unidad_medida: { enum: ["g", "kg", "ml", "l", "lb", "unidad"], description: "Unidad de medida estandarizada" },
        stock_actual: { bsonType: ["double", "int", "decimal"], minimum: 0, description: "Existencias en bodega" },
        stock_minimo: { bsonType: ["double", "int", "decimal"], minimum: 0, description: "Nivel de alerta mínima" },
        costo_unitario: { bsonType: ["double", "int", "decimal"], minimum: 0, description: "Costo unitario" },
        fecha_vencimiento: { bsonType: ["string", "date", "null"], description: "Fecha de vencimiento del lote" },
        estado: { enum: ["ACTIVO", "INACTIVO"], description: "Estado del insumo" }
      }
    }
  }
});

// 5. Colección: recetas
dbInstance.createCollection("recetas", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id_producto", "id_insumo", "cantidad"],
      properties: {
        id_producto: { bsonType: ["string", "objectId"], description: "Referencia al producto elaborado" },
        id_insumo: { bsonType: ["string", "objectId"], description: "Referencia al insumo requerido" },
        cantidad: { bsonType: ["double", "int", "decimal"], minimum: 0.0001, description: "Cantidad de insumo por unidad de producto" }
      }
    }
  }
});

// 6. Colección: proveedores
dbInstance.createCollection("proveedores", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["nit", "razon_social", "estado"],
      properties: {
        nit: { bsonType: "string", description: "NIT o documento único del proveedor" },
        razon_social: { bsonType: "string", description: "Razón social del proveedor" },
        telefono: { bsonType: "string" },
        correo: { bsonType: ["string", "null"] },
        direccion: { bsonType: "string" },
        estado: { enum: ["ACTIVO", "INACTIVO"], description: "Estado del proveedor" }
      }
    }
  }
});

// 7. Colección: compras
dbInstance.createCollection("compras", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["numero_factura", "fecha_compra", "id_proveedor", "id_usuario", "total", "detalle"],
      properties: {
        numero_factura: { bsonType: "string", description: "Número de factura único" },
        fecha_compra: { bsonType: ["string", "date"], description: "Fecha y hora de compra" },
        id_proveedor: { bsonType: ["string", "objectId"], description: "Referencia al proveedor" },
        id_usuario: { bsonType: ["string", "objectId"], description: "Usuario que registró la compra" },
        total: { bsonType: ["double", "int", "decimal"], minimum: 0, description: "Total de la compra" },
        detalle: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["id_insumo", "cantidad", "costo_unitario", "subtotal"],
            properties: {
              id_insumo: { bsonType: ["string", "objectId"] },
              cantidad: { bsonType: ["double", "int", "decimal"], minimum: 0.001 },
              costo_unitario: { bsonType: ["double", "int", "decimal"], minimum: 0 },
              subtotal: { bsonType: ["double", "int", "decimal"], minimum: 0 }
            }
          }
        }
      }
    }
  }
});

// 8. Colección: clientes
dbInstance.createCollection("clientes", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["identificacion", "nombres", "apellidos", "tipo_cliente", "estado"],
      properties: {
        identificacion: { bsonType: "string", description: "Documento único del cliente" },
        nombres: { bsonType: "string" },
        apellidos: { bsonType: "string" },
        telefono: { bsonType: "string" },
        correo: { bsonType: ["string", "null"] },
        tipo_cliente: { enum: ["APRENDIZ", "INSTRUCTOR", "FUNCIONARIO", "EXTERNO"] },
        estado: { enum: ["ACTIVO", "INACTIVO"] }
      }
    }
  }
});

// 9. Colección: pedidos
dbInstance.createCollection("pedidos", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["fecha_pedido", "id_cliente", "id_usuario", "tipo_pedido", "estado", "total", "detalle"],
      properties: {
        fecha_pedido: { bsonType: ["string", "date"] },
        id_cliente: { bsonType: ["string", "objectId"] },
        id_usuario: { bsonType: ["string", "objectId"] },
        tipo_pedido: { enum: ["MESA", "PARA_LLEVAR", "EVENTO"] },
        estado: { enum: ["PENDIENTE", "EN_PREPARACION", "ENTREGADO", "ANULADO"] },
        total: { bsonType: ["double", "int", "decimal"], minimum: 0 },
        observaciones: { bsonType: "string" },
        detalle: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["id_producto", "cantidad", "precio_unitario", "subtotal"],
            properties: {
              id_producto: { bsonType: ["string", "objectId"] },
              cantidad: { bsonType: ["double", "int", "decimal"], minimum: 0.01 },
              precio_unitario: { bsonType: ["double", "int", "decimal"], minimum: 0 },
              subtotal: { bsonType: ["double", "int", "decimal"], minimum: 0 }
            }
          }
        }
      }
    }
  }
});

// 10. Colección: calificaciones (MongoDB)
dbInstance.createCollection("calificaciones", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id_pedido", "id_cliente", "fecha", "calificacion_servicio", "productos"],
      properties: {
        id_pedido: { bsonType: ["string", "objectId"] },
        id_cliente: { bsonType: ["string", "objectId"] },
        fecha: { bsonType: ["string", "date"] },
        calificacion_servicio: { bsonType: "int", minimum: 1, maximum: 5 },
        comentario: { bsonType: "string" },
        productos: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["id_producto", "calificacion"],
            properties: {
              id_producto: { bsonType: ["string", "objectId"] },
              nombre: { bsonType: "string" },
              calificacion: { bsonType: "int", minimum: 1, maximum: 5 }
            }
          }
        }
      }
    }
  }
});

print("Colecciones y validaciones $jsonSchema creadas con éxito.");
