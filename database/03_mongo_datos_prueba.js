/**
 * Script 03: Inserción de Datos de Prueba Iniciales (DML) para MongoDB
 * Base de Datos: bd_gastronomia_nosql
 * Unidad Productiva de Gastronomía - CGDSS SENA
 * Contiene al menos 10 registros por cada entidad principal.
 */

const dbName = "bd_gastronomia_nosql";
const dbInstance = db.getSiblingDB(dbName);

print("Poblando datos de prueba en: " + dbName);

// 1. Limpieza opcional de colecciones previas
dbInstance.usuarios.deleteMany({});
dbInstance.categorias.deleteMany({});
dbInstance.productos.deleteMany({});
dbInstance.insumos.deleteMany({});
dbInstance.recetas.deleteMany({});
dbInstance.proveedores.deleteMany({});
dbInstance.compras.deleteMany({});
dbInstance.clientes.deleteMany({});
dbInstance.pedidos.deleteMany({});
dbInstance.calificaciones.deleteMany({});

// Hash bcrypt para 'admin123', 'cajero123', 'cocinero123'
const hashAdmin = "$2b$12$K8yXh6pQkY6Q.x7r7x8i0.0j4wA2e9R9W9hWJqg9Bq2t2e3x5y6zK"; // admin123
const hashCajero = "$2b$12$L8yXh6pQkY6Q.x7r7x8i0.0j4wA2e9R9W9hWJqg9Bq2t2e3x5y6zL"; // cajero123
const hashCocinero = "$2b$12$M8yXh6pQkY6Q.x7r7x8i0.0j4wA2e9R9W9hWJqg9Bq2t2e3x5y6zM"; // cocinero123

// 2. Insertar Usuarios (10 registros)
const usuariosDocs = [
  { identificacion: "1075200001", nombres: "Carlos Alberto", apellidos: "Mendoza Silva", correo: "admin@gastronomia.sena.edu.co", password: hashAdmin, rol: "ADMIN", estado: "ACTIVO" },
  { identificacion: "1075200002", nombres: "María Fernanda", apellidos: "Gómez Trujillo", correo: "cajero1@gastronomia.sena.edu.co", password: hashCajero, rol: "CAJERO", estado: "ACTIVO" },
  { identificacion: "1075200003", nombres: "Andrés Felipe", apellidos: "Castro Rojas", correo: "cajero2@gastronomia.sena.edu.co", password: hashCajero, rol: "CAJERO", estado: "ACTIVO" },
  { identificacion: "1075200004", nombres: "Javier Eduardo", apellidos: "Pérez Muñoz", correo: "cocinero1@gastronomia.sena.edu.co", password: hashCocinero, rol: "COCINERO", estado: "ACTIVO" },
  { identificacion: "1075200005", nombres: "Diana Marcela", apellidos: "Ramírez Ortiz", correo: "cocinero2@gastronomia.sena.edu.co", password: hashCocinero, rol: "COCINERO", estado: "ACTIVO" },
  { identificacion: "1075200006", nombres: "Juan José", apellidos: "Perdomo Trejos", correo: "jperdomo@gastronomia.sena.edu.co", password: hashAdmin, rol: "ADMIN", estado: "ACTIVO" },
  { identificacion: "1075200007", nombres: "Paola Andrea", apellidos: "Gutiérrez Vega", correo: "paola.cajero@gastronomia.sena.edu.co", password: hashCajero, rol: "CAJERO", estado: "ACTIVO" },
  { identificacion: "1075200008", nombres: "Wilson", apellidos: "Martínez Instructor", correo: "wmartinez@sena.edu.co", password: hashAdmin, rol: "ADMIN", estado: "ACTIVO" },
  { identificacion: "1075200009", nombres: "Héctor Fabio", apellidos: "López Salazar", correo: "hector.cocina@gastronomia.sena.edu.co", password: hashCocinero, rol: "COCINERO", estado: "ACTIVO" },
  { identificacion: "1075200010", nombres: "Lina Constanza", apellidos: "Vargas Medina", correo: "lina.inactiva@gastronomia.sena.edu.co", password: hashCajero, rol: "CAJERO", estado: "INACTIVO" }
];
const resUsuarios = dbInstance.usuarios.insertMany(usuariosDocs);
const uIds = Object.values(resUsuarios.insertedIds);

// 3. Insertar Categorías (10 registros)
const categoriasDocs = [
  { nombre: "Almuerzos Ejecutivos", descripcion: "Platos completos balanceados con proteína, carbohidrato y ensalada", estado: "ACTIVO" },
  { nombre: "Bebidas Naturales", descripcion: "Jugos de fruta fresca en agua y en leche", estado: "ACTIVO" },
  { nombre: "Bebidas Calientes", descripcion: "Café de origen, infusiones y chocolate", estado: "ACTIVO" },
  { nombre: "Panadería Artesanal", descripcion: "Panes tradicionales, hojaldres y croissants", estado: "ACTIVO" },
  { nombre: "Repostería y Postres", descripcion: "Tortas, mousses y cheesecakes", estado: "ACTIVO" },
  { nombre: "Comidas Rápidas", descripcion: "Hamburguesas artesanales, sándwiches y perros calientes", estado: "ACTIVO" },
  { nombre: "Ensaladas y Saludables", descripcion: "Bowls y ensaladas frescas con aderezos de la casa", estado: "ACTIVO" },
  { nombre: "Desayunos Tradicionales", descripcion: "Calentados, huevos al gusto y arepas", estado: "ACTIVO" },
  { nombre: "Pasabocas y Snacks", descripcion: "Empanadas, pasteles y deditos de queso", estado: "ACTIVO" },
  { nombre: "Menús Especiales Institucionales", descripcion: "Platos para eventos académicos y convenios", estado: "ACTIVO" }
];
const resCategorias = dbInstance.categorias.insertMany(categoriasDocs);
const cIds = Object.values(resCategorias.insertedIds);

// 4. Insertar Insumos (10 registros)
const insumosDocs = [
  { nombre: "Pechuga de pollo", unidad_medida: "kg", stock_actual: 45.5, stock_minimo: 10.0, costo_unitario: 14000.0, fecha_vencimiento: "2026-11-15", estado: "ACTIVO" },
  { nombre: "Carne de res magra", unidad_medida: "kg", stock_actual: 32.0, stock_minimo: 8.0, costo_unitario: 19500.0, fecha_vencimiento: "2026-11-10", estado: "ACTIVO" },
  { nombre: "Arroz blanco superior", unidad_medida: "kg", stock_actual: 80.0, stock_minimo: 20.0, costo_unitario: 3800.0, fecha_vencimiento: "2027-05-30", estado: "ACTIVO" },
  { nombre: "Pulpa de lulo fresco", unidad_medida: "kg", stock_actual: 15.0, stock_minimo: 5.0, costo_unitario: 8500.0, fecha_vencimiento: "2026-10-30", estado: "ACTIVO" },
  { nombre: "Pulpa de maracuyá", unidad_medida: "kg", stock_actual: 18.0, stock_minimo: 5.0, costo_unitario: 7800.0, fecha_vencimiento: "2026-11-05", estado: "ACTIVO" },
  { nombre: "Azúcar morena", unidad_medida: "kg", stock_actual: 50.0, stock_minimo: 15.0, costo_unitario: 4200.0, fecha_vencimiento: "2027-08-20", estado: "ACTIVO" },
  { nombre: "Leche entera pasteurizada", unidad_medida: "l", stock_actual: 30.0, stock_minimo: 10.0, costo_unitario: 3600.0, fecha_vencimiento: "2026-10-28", estado: "ACTIVO" },
  { nombre: "Harina de trigo especial", unidad_medida: "kg", stock_actual: 60.0, stock_minimo: 15.0, costo_unitario: 3500.0, fecha_vencimiento: "2027-02-15", estado: "ACTIVO" },
  { nombre: "Café especial Huila molido", unidad_medida: "kg", stock_actual: 22.0, stock_minimo: 5.0, costo_unitario: 28000.0, fecha_vencimiento: "2027-04-10", estado: "ACTIVO" },
  { nombre: "Queso campesino fresco", unidad_medida: "kg", stock_actual: 12.0, stock_minimo: 4.0, costo_unitario: 16000.0, fecha_vencimiento: "2026-10-26", estado: "ACTIVO" }
];
const resInsumos = dbInstance.insumos.insertMany(insumosDocs);
const iIds = Object.values(resInsumos.insertedIds);

// 5. Insertar Productos (10 registros)
const productosDocs = [
  { codigo: "PRD-001", nombre: "Almuerzo Ejecutivo Pollo a la Plancha", descripcion: "Pechuga a la plancha, arroz, ensalada fresca y sopa del día", precio_venta: 14000.0, unidad_venta: "Plato", id_categoria: cIds[0].toString(), estado: "DISPONIBLE" },
  { codigo: "PRD-002", nombre: "Almuerzo Ejecutivo Carne Asada", descripcion: "Corte de res a la parrilla, arroz, ensalada y sopa del día", precio_venta: 16000.0, unidad_venta: "Plato", id_categoria: cIds[0].toString(), estado: "DISPONIBLE" },
  { codigo: "PRD-003", nombre: "Jugo Natural de Lulo", descripcion: "Jugo refrescante preparado con fruta fresca en agua", precio_venta: 4000.0, unidad_venta: "Vaso 12oz", id_categoria: cIds[1].toString(), estado: "DISPONIBLE" },
  { codigo: "PRD-004", nombre: "Jugo Natural de Maracuyá", descripcion: "Delicioso jugo natural de maracuyá campesino", precio_venta: 4000.0, unidad_venta: "Vaso 12oz", id_categoria: cIds[1].toString(), estado: "DISPONIBLE" },
  { codigo: "PRD-005", nombre: "Café Espresso Doble Especial Huila", descripcion: "Extracción doble de café arábico especial de la región", precio_venta: 3500.0, unidad_venta: "Taza", id_categoria: cIds[2].toString(), estado: "DISPONIBLE" },
  { codigo: "PRD-006", nombre: "Croissant de Mantequilla", descripcion: "Croissant horneado diariamente por aprendices de panadería", precio_venta: 3000.0, unidad_venta: "Unidad", id_categoria: cIds[3].toString(), estado: "DISPONIBLE" },
  { codigo: "PRD-007", nombre: "Cheesecake de Frutos Rojos", descripcion: "Porción de postre artesanal suave con coulis de mora y fresa", precio_venta: 6500.0, unidad_venta: "Porción", id_categoria: cIds[4].toString(), estado: "DISPONIBLE" },
  { codigo: "PRD-008", nombre: "Hamburguesa Artesanal Gastronomía", descripcion: "Carne de res 150g, queso campesino, lechuga y salsa especial", precio_venta: 15000.0, unidad_venta: "Unidad", id_categoria: cIds[5].toString(), estado: "DISPONIBLE" },
  { codigo: "PRD-009", nombre: "Ensalada César con Pollo Grillé", descripcion: "Mix de lechugas, pechuga salteada, crutones y aderezo césar", precio_venta: 12000.0, unidad_venta: "Bowl", id_categoria: cIds[6].toString(), estado: "DISPONIBLE" },
  { codigo: "PRD-010", nombre: "Desayuno Tradicional Campesino", descripcion: "Huevos al gusto, calentado de arroz y café caliente", precio_venta: 9500.0, unidad_venta: "Plato", id_categoria: cIds[7].toString(), estado: "DISPONIBLE" }
];
const resProductos = dbInstance.productos.insertMany(productosDocs);
const pIds = Object.values(resProductos.insertedIds);

// 6. Insertar Recetas (Fichas Técnicas)
const recetasDocs = [
  // PRD-001 (Almuerzo Pollo): Pechuga (0.22 kg), Arroz (0.10 kg)
  { id_producto: pIds[0].toString(), id_insumo: iIds[0].toString(), cantidad: 0.22 },
  { id_producto: pIds[0].toString(), id_insumo: iIds[2].toString(), cantidad: 0.10 },
  // PRD-002 (Almuerzo Res): Carne (0.25 kg), Arroz (0.10 kg)
  { id_producto: pIds[1].toString(), id_insumo: iIds[1].toString(), cantidad: 0.25 },
  { id_producto: pIds[1].toString(), id_insumo: iIds[2].toString(), cantidad: 0.10 },
  // PRD-003 (Jugo Lulo): Lulo (0.12 kg), Azúcar (0.03 kg)
  { id_producto: pIds[2].toString(), id_insumo: iIds[3].toString(), cantidad: 0.12 },
  { id_producto: pIds[2].toString(), id_insumo: iIds[5].toString(), cantidad: 0.03 },
  // PRD-004 (Jugo Maracuyá): Maracuyá (0.12 kg), Azúcar (0.03 kg)
  { id_producto: pIds[3].toString(), id_insumo: iIds[4].toString(), cantidad: 0.12 },
  { id_producto: pIds[3].toString(), id_insumo: iIds[5].toString(), cantidad: 0.03 },
  // PRD-005 (Café Espresso): Café (0.018 kg)
  { id_producto: pIds[4].toString(), id_insumo: iIds[8].toString(), cantidad: 0.018 },
  // PRD-006 (Croissant): Harina (0.08 kg), Leche (0.04 l)
  { id_producto: pIds[5].toString(), id_insumo: iIds[7].toString(), cantidad: 0.08 },
  { id_producto: pIds[5].toString(), id_insumo: iIds[6].toString(), cantidad: 0.04 },
  // PRD-008 (Hamburguesa): Carne (0.16 kg), Queso (0.05 kg)
  { id_producto: pIds[7].toString(), id_insumo: iIds[1].toString(), cantidad: 0.16 },
  { id_producto: pIds[7].toString(), id_insumo: iIds[9].toString(), cantidad: 0.05 }
];
dbInstance.recetas.insertMany(recetasDocs);

// 7. Insertar Proveedores (10 registros)
const proveedoresDocs = [
  { nit: "900123456-1", razon_social: "Avícola Central del Huila S.A.S.", telefono: "3114567890", correo: "ventas@avicolahuila.com", direccion: "Km 2 Vía Neiva - Pitalito", estado: "ACTIVO" },
  { nit: "900654321-2", razon_social: "Frigorífico y Carnes del Sur Ltda.", telefono: "3127891234", correo: "contacto@carnesdelsur.com", direccion: "Zona Industrial Pitalito", estado: "ACTIVO" },
  { nit: "800345678-3", razon_social: "Asociación Campesina Frutas del Valle", telefono: "3156789012", correo: "frutasdelvalle@agrohuila.org", direccion: "Plaza Mayorista Bodega 4", estado: "ACTIVO" },
  { nit: "890123789-4", razon_social: "Lácteos y Quesos San Pedro", telefono: "3103456789", correo: "lacteossanpedro@gmail.com", direccion: "Calle 10 # 5-20 Pitalito", estado: "ACTIVO" },
  { nit: "860456123-5", razon_social: "Molinos Harineros de Colombia S.A.", telefono: "3189012345", correo: "pedidos@molinoshdc.com", direccion: "Carrera 4 # 12-40", estado: "ACTIVO" },
  { nit: "901234567-6", razon_social: "Federación Cafetera Especial Huila", telefono: "3201234567", correo: "cafehuilaespecial@federacion.com", direccion: "Calle 8 # 2-15", estado: "ACTIVO" },
  { nit: "890567890-7", razon_social: "Abarrotes y Alimentos El Triunfo", telefono: "3145678901", correo: "ventas@abarrotestriunfo.com", direccion: "Avenida Pastrana # 8-30", estado: "ACTIVO" },
  { nit: "900789012-8", razon_social: "Grasas y Aceites Naturales S.A.", telefono: "3178901234", correo: "comercial@grasasnaturales.co", direccion: "Km 5 Vía San Agustín", estado: "ACTIVO" },
  { nit: "901345678-9", razon_social: "Empaques Ecológicos del Sur", telefono: "3134567890", correo: "ecoempaques@verde.com", direccion: "Carrera 1 # 15-20", estado: "ACTIVO" },
  { nit: "900987654-0", razon_social: "Insumos y Víveres La Sabana", telefono: "3167890123", correo: "sabana.viveres@gmail.com", direccion: "Calle 15 # 3-12", estado: "ACTIVO" }
];
const resProveedores = dbInstance.proveedores.insertMany(proveedoresDocs);
const provIds = Object.values(resProveedores.insertedIds);

// 8. Insertar Clientes (10 registros)
const clientesDocs = [
  { identificacion: "1083900001", nombres: "Valentina", apellidos: "Dussán Polanía", telefono: "3123456780", correo: "valentina.dussan@misena.edu.co", tipo_cliente: "APRENDIZ", estado: "ACTIVO" },
  { identificacion: "1083900002", nombres: "Mateo", apellidos: "Hernández Claros", telefono: "3145678901", correo: "mateo.hernandez@misena.edu.co", tipo_cliente: "APRENDIZ", estado: "ACTIVO" },
  { identificacion: "1234500003", nombres: "Hernando", apellidos: "Cabrera Silva", telefono: "3156789012", correo: "hcabrera@sena.edu.co", tipo_cliente: "INSTRUCTOR", estado: "ACTIVO" },
  { identificacion: "1234500004", nombres: "Gloria Esperanza", apellidos: "Mora Tovar", telefono: "3167890123", correo: "gmora@sena.edu.co", tipo_cliente: "INSTRUCTOR", estado: "ACTIVO" },
  { identificacion: "5523400005", nombres: "Alfonso", apellidos: "Bravo Meneses", telefono: "3178901234", correo: "abravo@sena.edu.co", tipo_cliente: "FUNCIONARIO", estado: "ACTIVO" },
  { identificacion: "5523400006", nombres: "Sonia Patricia", apellidos: "Cuéllar Leiva", telefono: "3189012345", correo: "scuellar@sena.edu.co", tipo_cliente: "FUNCIONARIO", estado: "ACTIVO" },
  { identificacion: "1075300007", nombres: "Camilo Andrés", apellidos: "Torres Bermeo", telefono: "3190123456", correo: "camilo.torres@gmail.com", tipo_cliente: "EXTERNO", estado: "ACTIVO" },
  { identificacion: "1075300008", nombres: "Claudia Milena", apellidos: "Sánchez Vargas", telefono: "3101234567", correo: "claudia.sanchez@hotmail.com", tipo_cliente: "EXTERNO", estado: "ACTIVO" },
  { identificacion: "1083900009", nombres: "Daniel Felipe", apellidos: "Ospina Rincón", telefono: "3112345678", correo: "dospina@misena.edu.co", tipo_cliente: "APRENDIZ", estado: "ACTIVO" },
  { identificacion: "1083900010", nombres: "Laura Sofía", apellidos: "Méndez Chávarro", telefono: "3133456789", correo: "lmendez@misena.edu.co", tipo_cliente: "APRENDIZ", estado: "INACTIVO" }
];
const resClientes = dbInstance.clientes.insertMany(clientesDocs);
const cliIds = Object.values(resClientes.insertedIds);

// 9. Insertar Compras (10 registros con detalle)
const comprasDocs = [
  { numero_factura: "FAC-PROV-001", fecha_compra: "2026-10-15T08:30:00", id_proveedor: provIds[0].toString(), id_usuario: uIds[0].toString(), total: 280000.0, detalle: [{ id_insumo: iIds[0].toString(), cantidad: 20.0, costo_unitario: 14000.0, subtotal: 280000.0 }] },
  { numero_factura: "FAC-PROV-002", fecha_compra: "2026-10-15T09:15:00", id_proveedor: provIds[1].toString(), id_usuario: uIds[0].toString(), total: 292500.0, detalle: [{ id_insumo: iIds[1].toString(), cantidad: 15.0, costo_unitario: 19500.0, subtotal: 292500.0 }] },
  { numero_factura: "FAC-PROV-003", fecha_compra: "2026-10-16T10:00:00", id_proveedor: provIds[2].toString(), id_usuario: uIds[0].toString(), total: 163000.0, detalle: [{ id_insumo: iIds[3].toString(), cantidad: 10.0, costo_unitario: 8500.0, subtotal: 85000.0 }, { id_insumo: iIds[4].toString(), cantidad: 10.0, costo_unitario: 7800.0, subtotal: 78000.0 }] },
  { numero_factura: "FAC-PROV-004", fecha_compra: "2026-10-16T11:20:00", id_proveedor: provIds[6].toString(), id_usuario: uIds[0].toString(), total: 276000.0, detalle: [{ id_insumo: iIds[2].toString(), cantidad: 40.0, costo_unitario: 3800.0, subtotal: 152000.0 }, { id_insumo: iIds[5].toString(), cantidad: 20.0, costo_unitario: 4200.0, subtotal: 84000.0 }] },
  { numero_factura: "FAC-PROV-005", fecha_compra: "2026-10-17T08:00:00", id_proveedor: provIds[3].toString(), id_usuario: uIds[0].toString(), total: 172000.0, detalle: [{ id_insumo: iIds[6].toString(), cantidad: 20.0, costo_unitario: 3600.0, subtotal: 72000.0 }, { id_insumo: iIds[9].toString(), cantidad: 10.0, costo_unitario: 10000.0, subtotal: 100000.0 }] },
  { numero_factura: "FAC-PROV-006", fecha_compra: "2026-10-17T14:30:00", id_proveedor: provIds[4].toString(), id_usuario: uIds[0].toString(), total: 105000.0, detalle: [{ id_insumo: iIds[7].toString(), cantidad: 30.0, costo_unitario: 3500.0, subtotal: 105000.0 }] },
  { numero_factura: "FAC-PROV-007", fecha_compra: "2026-10-18T09:00:00", id_proveedor: provIds[5].toString(), id_usuario: uIds[0].toString(), total: 280000.0, detalle: [{ id_insumo: iIds[8].toString(), cantidad: 10.0, costo_unitario: 28000.0, subtotal: 280000.0 }] },
  { numero_factura: "FAC-PROV-008", fecha_compra: "2026-10-18T16:00:00", id_proveedor: provIds[0].toString(), id_usuario: uIds[0].toString(), total: 140000.0, detalle: [{ id_insumo: iIds[0].toString(), cantidad: 10.0, costo_unitario: 14000.0, subtotal: 140000.0 }] },
  { numero_factura: "FAC-PROV-009", fecha_compra: "2026-10-19T08:30:00", id_proveedor: provIds[1].toString(), id_usuario: uIds[0].toString(), total: 195000.0, detalle: [{ id_insumo: iIds[1].toString(), cantidad: 10.0, costo_unitario: 19500.0, subtotal: 195000.0 }] },
  { numero_factura: "FAC-PROV-010", fecha_compra: "2026-10-19T10:45:00", id_proveedor: provIds[3].toString(), id_usuario: uIds[0].toString(), total: 144000.0, detalle: [{ id_insumo: iIds[6].toString(), cantidad: 40.0, costo_unitario: 3600.0, subtotal: 144000.0 }] }
];
dbInstance.compras.insertMany(comprasDocs);

// 10. Insertar Pedidos (10 registros con estados diversos)
const pedidosDocs = [
  { fecha_pedido: "2026-10-19T12:00:00", id_cliente: cliIds[0].toString(), id_usuario: uIds[1].toString(), tipo_pedido: "MESA", estado: "ENTREGADO", total: 18000.0, observaciones: "Mesa 4", detalle: [{ id_producto: pIds[0].toString(), cantidad: 1.0, precio_unitario: 14000.0, subtotal: 14000.0 }, { id_producto: pIds[2].toString(), cantidad: 1.0, precio_unitario: 4000.0, subtotal: 4000.0 }] },
  { fecha_pedido: "2026-10-19T12:15:00", id_cliente: cliIds[1].toString(), id_usuario: uIds[1].toString(), tipo_pedido: "PARA_LLEVAR", estado: "ENTREGADO", total: 20000.0, observaciones: "Empacar salsa aparte", detalle: [{ id_producto: pIds[1].toString(), cantidad: 1.0, precio_unitario: 16000.0, subtotal: 16000.0 }, { id_producto: pIds[3].toString(), cantidad: 1.0, precio_unitario: 4000.0, subtotal: 4000.0 }] },
  { fecha_pedido: "2026-10-19T12:30:00", id_cliente: cliIds[2].toString(), id_usuario: uIds[2].toString(), tipo_pedido: "MESA", estado: "ENTREGADO", total: 17500.0, observaciones: "Mesa 1", detalle: [{ id_producto: pIds[0].toString(), cantidad: 1.0, precio_unitario: 14000.0, subtotal: 14000.0 }, { id_producto: pIds[4].toString(), cantidad: 1.0, precio_unitario: 3500.0, subtotal: 3500.0 }] },
  { fecha_pedido: "2026-10-20T08:30:00", id_cliente: cliIds[3].toString(), id_usuario: uIds[1].toString(), tipo_pedido: "MESA", estado: "ENTREGADO", total: 12500.0, observaciones: "Café con poca azúcar", detalle: [{ id_producto: pIds[9].toString(), cantidad: 1.0, precio_unitario: 9500.0, subtotal: 9500.0 }, { id_producto: pIds[5].toString(), cantidad: 1.0, precio_unitario: 3000.0, subtotal: 3000.0 }] },
  { fecha_pedido: "2026-10-20T10:00:00", id_cliente: cliIds[4].toString(), id_usuario: uIds[2].toString(), tipo_pedido: "PARA_LLEVAR", estado: "ENTREGADO", total: 9500.0, observaciones: "Para refrigerio de reunión", detalle: [{ id_producto: pIds[5].toString(), cantidad: 1.0, precio_unitario: 3000.0, subtotal: 3000.0 }, { id_producto: pIds[6].toString(), cantidad: 1.0, precio_unitario: 6500.0, subtotal: 6500.0 }] },
  { fecha_pedido: "2026-10-20T12:10:00", id_cliente: cliIds[5].toString(), id_usuario: uIds[1].toString(), tipo_pedido: "MESA", estado: "EN_PREPARACION", total: 19000.0, observaciones: "Mesa 8", detalle: [{ id_producto: pIds[7].toString(), cantidad: 1.0, precio_unitario: 15000.0, subtotal: 15000.0 }, { id_producto: pIds[2].toString(), cantidad: 1.0, precio_unitario: 4000.0, subtotal: 4000.0 }] },
  { fecha_pedido: "2026-10-20T12:20:00", id_cliente: cliIds[6].toString(), id_usuario: uIds[2].toString(), tipo_pedido: "EVENTO", estado: "PENDIENTE", total: 140000.0, observaciones: "10 almuerzos para auditorio", detalle: [{ id_producto: pIds[0].toString(), cantidad: 10.0, precio_unitario: 14000.0, subtotal: 140000.0 }] },
  { fecha_pedido: "2026-10-20T12:45:00", id_cliente: cliIds[7].toString(), id_usuario: uIds[1].toString(), tipo_pedido: "MESA", estado: "PENDIENTE", total: 16000.0, observaciones: "Mesa 2", detalle: [{ id_producto: pIds[8].toString(), cantidad: 1.0, precio_unitario: 12000.0, subtotal: 12000.0 }, { id_producto: pIds[3].toString(), cantidad: 1.0, precio_unitario: 4000.0, subtotal: 4000.0 }] },
  { fecha_pedido: "2026-10-20T13:00:00", id_cliente: cliIds[8].toString(), id_usuario: uIds[1].toString(), tipo_pedido: "MESA", estado: "ANULADO", total: 14000.0, observaciones: "Cliente canceló por tiempo", detalle: [{ id_producto: pIds[0].toString(), cantidad: 1.0, precio_unitario: 14000.0, subtotal: 14000.0 }] },
  { fecha_pedido: "2026-10-21T09:15:00", id_cliente: cliIds[0].toString(), id_usuario: uIds[1].toString(), tipo_pedido: "PARA_LLEVAR", estado: "PENDIENTE", total: 10000.0, observaciones: "", detalle: [{ id_producto: pIds[4].toString(), cantidad: 2.0, precio_unitario: 3500.0, subtotal: 7000.0 }, { id_producto: pIds[5].toString(), cantidad: 1.0, precio_unitario: 3000.0, subtotal: 3000.0 }] }
];
const resPedidos = dbInstance.pedidos.insertMany(pedidosDocs);
const pedIds = Object.values(resPedidos.insertedIds);

// 11. Insertar Calificaciones (10 registros en MongoDB)
const calificacionesDocs = [
  { id_pedido: pedIds[0].toString(), id_cliente: cliIds[0].toString(), fecha: "2026-10-19T13:00:00", calificacion_servicio: 5, comentario: "Excelente atención y sazón, el pollo en su punto perfecto.", productos: [{ id_producto: pIds[0].toString(), nombre: "Almuerzo Pollo a la Plancha", calificacion: 5 }, { id_producto: pIds[2].toString(), nombre: "Jugo Natural de Lulo", calificacion: 5 }] },
  { id_pedido: pedIds[1].toString(), id_cliente: cliIds[1].toString(), fecha: "2026-10-19T13:15:00", calificacion_servicio: 4, comentario: "Muy rica la carne, empaque muy seguro.", productos: [{ id_producto: pIds[1].toString(), nombre: "Almuerzo Carne Asada", calificacion: 4 }, { id_producto: pIds[3].toString(), nombre: "Jugo Natural de Maracuyá", calificacion: 5 }] },
  { id_pedido: pedIds[2].toString(), id_cliente: cliIds[2].toString(), fecha: "2026-10-19T13:30:00", calificacion_servicio: 5, comentario: "El café huilense tiene notas espectaculares.", productos: [{ id_producto: pIds[0].toString(), nombre: "Almuerzo Pollo a la Plancha", calificacion: 5 }, { id_producto: pIds[4].toString(), nombre: "Café Espresso Doble", calificacion: 5 }] },
  { id_pedido: pedIds[3].toString(), id_cliente: cliIds[3].toString(), fecha: "2026-10-20T09:15:00", calificacion_servicio: 5, comentario: "Desayuno muy completo, el croissant recién horneado estaba crocante.", productos: [{ id_producto: pIds[9].toString(), nombre: "Desayuno Tradicional", calificacion: 5 }, { id_producto: pIds[5].toString(), nombre: "Croissant de Mantequilla", calificacion: 5 }] },
  { id_pedido: pedIds[4].toString(), id_cliente: cliIds[4].toString(), fecha: "2026-10-20T10:45:00", calificacion_servicio: 4, comentario: "Buen postre, aunque podría tener un poco más de coulis.", productos: [{ id_producto: pIds[6].toString(), nombre: "Cheesecake de Frutos Rojos", calificacion: 4 }] },
  { id_pedido: pedIds[0].toString(), id_cliente: cliIds[2].toString(), fecha: "2026-10-20T11:00:00", calificacion_servicio: 5, comentario: "Excelente iniciativa gastronómica del SENA.", productos: [{ id_producto: pIds[2].toString(), nombre: "Jugo Natural de Lulo", calificacion: 5 }] },
  { id_pedido: pedIds[1].toString(), id_cliente: cliIds[3].toString(), fecha: "2026-10-20T11:30:00", calificacion_servicio: 5, comentario: "La carne asada estuvo suave y jugosa.", productos: [{ id_producto: pIds[1].toString(), nombre: "Almuerzo Carne Asada", calificacion: 5 }] },
  { id_pedido: pedIds[2].toString(), id_cliente: cliIds[4].toString(), fecha: "2026-10-20T12:00:00", calificacion_servicio: 4, comentario: "Buena atención de los aprendices cajeros.", productos: [{ id_producto: pIds[0].toString(), nombre: "Almuerzo Pollo a la Plancha", calificacion: 4 }] },
  { id_pedido: pedIds[3].toString(), id_cliente: cliIds[5].toString(), fecha: "2026-10-20T12:30:00", calificacion_servicio: 5, comentario: "Rapidez en la entrega y comida caliente.", productos: [{ id_producto: pIds[5].toString(), nombre: "Croissant de Mantequilla", calificacion: 5 }] },
  { id_pedido: pedIds[4].toString(), id_cliente: cliIds[6].toString(), fecha: "2026-10-20T13:00:00", calificacion_servicio: 4, comentario: "Presentación impecable de los platos.", productos: [{ id_producto: pIds[6].toString(), nombre: "Cheesecake de Frutos Rojos", calificacion: 4 }] }
];
dbInstance.calificaciones.insertMany(calificacionesDocs);

print("Datos de prueba sembrados exitosamente (mínimo 10 registros por colección).");
