/**
 * Script 02: Creación de Índices Únicos y de Rendimiento en MongoDB
 * Base de Datos: bd_gastronomia_nosql
 * Unidad Productiva de Gastronomía - CGDSS SENA
 */

const dbName = "bd_gastronomia_nosql";
const dbInstance = db.getSiblingDB(dbName);

print("Iniciando creación de índices en: " + dbName);

// 1. Índices en usuarios
dbInstance.usuarios.createIndex({ correo: 1 }, { unique: true, name: "idx_usuarios_correo_unique" });
dbInstance.usuarios.createIndex({ identificacion: 1 }, { unique: true, name: "idx_usuarios_identificacion_unique" });
dbInstance.usuarios.createIndex({ rol: 1 }, { name: "idx_usuarios_rol" });
dbInstance.usuarios.createIndex({ estado: 1 }, { name: "idx_usuarios_estado" });

// 2. Índices en categorias
dbInstance.categorias.createIndex({ nombre: 1 }, { unique: true, name: "idx_categorias_nombre_unique" });
dbInstance.categorias.createIndex({ estado: 1 }, { name: "idx_categorias_estado" });

// 3. Índices en productos
dbInstance.productos.createIndex({ codigo: 1 }, { unique: true, name: "idx_productos_codigo_unique" });
dbInstance.productos.createIndex({ id_categoria: 1 }, { name: "idx_productos_categoria" });
dbInstance.productos.createIndex({ estado: 1 }, { name: "idx_productos_estado" });
dbInstance.productos.createIndex({ nombre: 1 }, { name: "idx_productos_nombre" });

// 4. Índices en insumos
dbInstance.insumos.createIndex({ nombre: 1 }, { unique: true, name: "idx_insumos_nombre_unique" });
dbInstance.insumos.createIndex({ stock_actual: 1 }, { name: "idx_insumos_stock_actual" });
dbInstance.insumos.createIndex({ fecha_vencimiento: 1 }, { name: "idx_insumos_fecha_vencimiento" });
dbInstance.insumos.createIndex({ estado: 1 }, { name: "idx_insumos_estado" });

// 5. Índices en recetas
dbInstance.recetas.createIndex({ id_producto: 1, id_insumo: 1 }, { unique: true, name: "idx_recetas_prod_ins_unique" });
dbInstance.recetas.createIndex({ id_insumo: 1 }, { name: "idx_recetas_insumo" });

// 6. Índices en proveedores
dbInstance.proveedores.createIndex({ nit: 1 }, { unique: true, name: "idx_proveedores_nit_unique" });
dbInstance.proveedores.createIndex({ estado: 1 }, { name: "idx_proveedores_estado" });

// 7. Índices en compras
dbInstance.compras.createIndex({ numero_factura: 1 }, { unique: true, name: "idx_compras_factura_unique" });
dbInstance.compras.createIndex({ id_proveedor: 1 }, { name: "idx_compras_proveedor" });
dbInstance.compras.createIndex({ id_usuario: 1 }, { name: "idx_compras_usuario" });
dbInstance.compras.createIndex({ fecha_compra: -1 }, { name: "idx_compras_fecha" });
dbInstance.compras.createIndex({ "detalle.id_insumo": 1 }, { name: "idx_compras_detalle_insumo" });

// 8. Índices en clientes
dbInstance.clientes.createIndex({ identificacion: 1 }, { unique: true, name: "idx_clientes_identificacion_unique" });
dbInstance.clientes.createIndex({ tipo_cliente: 1 }, { name: "idx_clientes_tipo" });
dbInstance.clientes.createIndex({ estado: 1 }, { name: "idx_clientes_estado" });

// 9. Índices en pedidos
dbInstance.pedidos.createIndex({ id_cliente: 1 }, { name: "idx_pedidos_cliente" });
dbInstance.pedidos.createIndex({ id_usuario: 1 }, { name: "idx_pedidos_usuario" });
dbInstance.pedidos.createIndex({ estado: 1 }, { name: "idx_pedidos_estado" });
dbInstance.pedidos.createIndex({ fecha_pedido: -1 }, { name: "idx_pedidos_fecha" });
dbInstance.pedidos.createIndex({ "detalle.id_producto": 1 }, { name: "idx_pedidos_detalle_producto" });

// 10. Índices en calificaciones (MongoDB)
dbInstance.calificaciones.createIndex({ id_pedido: 1 }, { name: "idx_calificaciones_pedido" });
dbInstance.calificaciones.createIndex({ id_cliente: 1 }, { name: "idx_calificaciones_cliente" });
dbInstance.calificaciones.createIndex({ "productos.id_producto": 1 }, { name: "idx_calificaciones_producto" });
dbInstance.calificaciones.createIndex({ fecha: -1 }, { name: "idx_calificaciones_fecha" });

print("Índices creados exitosamente en todas las colecciones.");
