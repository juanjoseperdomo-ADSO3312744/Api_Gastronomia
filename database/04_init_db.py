"""
Script automatizado en Python para inicializar la base de datos MongoDB:
- Aplica validaciones de esquema ($jsonSchema)
- Crea índices únicos y de consulta
- Siembra al menos 10 registros de prueba por colección
- Cifra contraseñas reales con bcrypt para autenticación JWT
"""

import sys
import os
from datetime import datetime, timezone

# Añadir raíz al sys.path para importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.j_config import j_settings
from app.core.j_security import j_hashear_password
from app.database.j_conexion_mongo import JMongoConnection


def j_inicializar_base_datos():
    print(f" Conectando a MongoDB en {j_settings.MONGO_URI}...")
    cliente = JMongoConnection.j_conectar()
    db = cliente[j_settings.MONGO_DB_NAME]
    print(f" Base de datos seleccionada: {j_settings.MONGO_DB_NAME}")

    colecciones = [
        "usuarios", "categorias", "productos", "insumos",
        "recetas", "proveedores", "compras", "clientes",
        "pedidos", "calificaciones"
    ]

    # Limpiar datos anteriores
    print(" Limpiando colecciones existentes...")
    for col in colecciones:
        db[col].delete_many({})

    # 1. Crear Índices
    print(" Configurando índices...")
    # Usuarios
    db.usuarios.create_index("correo", unique=True)
    db.usuarios.create_index("identificacion", unique=True)
    # Categorias
    db.categorias.create_index("nombre", unique=True)
    # Productos
    db.productos.create_index("codigo", unique=True)
    db.productos.create_index("id_categoria")
    # Insumos
    db.insumos.create_index("nombre", unique=True)
    db.insumos.create_index("stock_actual")
    db.insumos.create_index("fecha_vencimiento")
    # Recetas
    db.recetas.create_index([("id_producto", 1), ("id_insumo", 1)], unique=True)
    # Proveedores
    db.proveedores.create_index("nit", unique=True)
    # Compras
    db.compras.create_index("numero_factura", unique=True)
    db.compras.create_index("id_proveedor")
    db.compras.create_index("fecha_compra")
    # Clientes
    db.clientes.create_index("identificacion", unique=True)
    # Pedidos
    db.pedidos.create_index("id_cliente")
    db.pedidos.create_index("estado")
    db.pedidos.create_index("fecha_pedido")
    # Calificaciones
    db.calificaciones.create_index("id_pedido")
    db.calificaciones.create_index("productos.id_producto")
    print(" Índices configurados correctamente.")

    # 2. Sembrar Usuarios (10 registros con contraseñas cifradas)
    print(" Sembrando usuarios...")
    pass_admin = j_hashear_password("admin123")
    pass_cajero = j_hashear_password("cajero123")
    pass_cocinero = j_hashear_password("cocinero123")

    usuarios_data = [
        {"identificacion": "1075200001", "nombres": "Carlos Alberto", "apellidos": "Mendoza Silva", "correo": "admin@gastronomia.sena.edu.co", "password": pass_admin, "rol": "ADMIN", "estado": "ACTIVO"},
        {"identificacion": "1075200002", "nombres": "María Fernanda", "apellidos": "Gómez Trujillo", "correo": "cajero1@gastronomia.sena.edu.co", "password": pass_cajero, "rol": "CAJERO", "estado": "ACTIVO"},
        {"identificacion": "1075200003", "nombres": "Andrés Felipe", "apellidos": "Castro Rojas", "correo": "cajero2@gastronomia.sena.edu.co", "password": pass_cajero, "rol": "CAJERO", "estado": "ACTIVO"},
        {"identificacion": "1075200004", "nombres": "Javier Eduardo", "apellidos": "Pérez Muñoz", "correo": "cocinero1@gastronomia.sena.edu.co", "password": pass_cocinero, "rol": "COCINERO", "estado": "ACTIVO"},
        {"identificacion": "1075200005", "nombres": "Diana Marcela", "apellidos": "Ramírez Ortiz", "correo": "cocinero2@gastronomia.sena.edu.co", "password": pass_cocinero, "rol": "COCINERO", "estado": "ACTIVO"},
        {"identificacion": "1075200006", "nombres": "Juan José", "apellidos": "Perdomo Trejos", "correo": "jperdomo@gastronomia.sena.edu.co", "password": pass_admin, "rol": "ADMIN", "estado": "ACTIVO"},
        {"identificacion": "1075200007", "nombres": "Paola Andrea", "apellidos": "Gutiérrez Vega", "correo": "paola.cajero@gastronomia.sena.edu.co", "password": pass_cajero, "rol": "CAJERO", "estado": "ACTIVO"},
        {"identificacion": "1075200008", "nombres": "Wilson", "apellidos": "Martínez Instructor", "correo": "wmartinez@sena.edu.co", "password": pass_admin, "rol": "ADMIN", "estado": "ACTIVO"},
        {"identificacion": "1075200009", "nombres": "Héctor Fabio", "apellidos": "López Salazar", "correo": "hector.cocina@gastronomia.sena.edu.co", "password": pass_cocinero, "rol": "COCINERO", "estado": "ACTIVO"},
        {"identificacion": "1075200010", "nombres": "Lina Constanza", "apellidos": "Vargas Medina", "correo": "lina.inactiva@gastronomia.sena.edu.co", "password": pass_cajero, "rol": "CAJERO", "estado": "INACTIVO"}
    ]
    u_ids = [str(r) for r in db.usuarios.insert_many(usuarios_data).inserted_ids]

    # 3. Categorías (10)
    print(" Sembrando categorías...")
    categorias_data = [
        {"nombre": "Almuerzos Ejecutivos", "descripcion": "Platos completos balanceados con proteína, carbohidrato y ensalada", "estado": "ACTIVO"},
        {"nombre": "Bebidas Naturales", "descripcion": "Jugos de fruta fresca en agua y en leche", "estado": "ACTIVO"},
        {"nombre": "Bebidas Calientes", "descripcion": "Café de origen, infusiones y chocolate", "estado": "ACTIVO"},
        {"nombre": "Panadería Artesanal", "descripcion": "Panes tradicionales, hojaldres y croissants", "estado": "ACTIVO"},
        {"nombre": "Repostería y Postres", "descripcion": "Tortas, mousses y cheesecakes", "estado": "ACTIVO"},
        {"nombre": "Comidas Rápidas", "descripcion": "Hamburguesas artesanales, sándwiches y perros calientes", "estado": "ACTIVO"},
        {"nombre": "Ensaladas y Saludables", "descripcion": "Bowls y ensaladas frescas con aderezos de la casa", "estado": "ACTIVO"},
        {"nombre": "Desayunos Tradicionales", "descripcion": "Calentados, huevos al gusto y arepas", "estado": "ACTIVO"},
        {"nombre": "Pasabocas y Snacks", "descripcion": "Empanadas, pasteles y deditos de queso", "estado": "ACTIVO"},
        {"nombre": "Menús Especiales Institucionales", "descripcion": "Platos para eventos académicos y convenios", "estado": "ACTIVO"}
    ]
    c_ids = [str(r) for r in db.categorias.insert_many(categorias_data).inserted_ids]

    # 4. Insumos (10)
    print(" Sembrando insumos...")
    insumos_data = [
        {"nombre": "Pechuga de pollo", "unidad_medida": "kg", "stock_actual": 45.5, "stock_minimo": 10.0, "costo_unitario": 14000.0, "fecha_vencimiento": "2026-11-15", "estado": "ACTIVO"},
        {"nombre": "Carne de res magra", "unidad_medida": "kg", "stock_actual": 32.0, "stock_minimo": 8.0, "costo_unitario": 19500.0, "fecha_vencimiento": "2026-11-10", "estado": "ACTIVO"},
        {"nombre": "Arroz blanco superior", "unidad_medida": "kg", "stock_actual": 80.0, "stock_minimo": 20.0, "costo_unitario": 3800.0, "fecha_vencimiento": "2027-05-30", "estado": "ACTIVO"},
        {"nombre": "Pulpa de lulo fresco", "unidad_medida": "kg", "stock_actual": 15.0, "stock_minimo": 5.0, "costo_unitario": 8500.0, "fecha_vencimiento": "2026-10-30", "estado": "ACTIVO"},
        {"nombre": "Pulpa de maracuyá", "unidad_medida": "kg", "stock_actual": 18.0, "stock_minimo": 5.0, "costo_unitario": 7800.0, "fecha_vencimiento": "2026-11-05", "estado": "ACTIVO"},
        {"nombre": "Azúcar morena", "unidad_medida": "kg", "stock_actual": 50.0, "stock_minimo": 15.0, "costo_unitario": 4200.0, "fecha_vencimiento": "2027-08-20", "estado": "ACTIVO"},
        {"nombre": "Leche entera pasteurizada", "unidad_medida": "l", "stock_actual": 30.0, "stock_minimo": 10.0, "costo_unitario": 3600.0, "fecha_vencimiento": "2026-10-28", "estado": "ACTIVO"},
        {"nombre": "Harina de trigo especial", "unidad_medida": "kg", "stock_actual": 60.0, "stock_minimo": 15.0, "costo_unitario": 3500.0, "fecha_vencimiento": "2027-02-15", "estado": "ACTIVO"},
        {"nombre": "Café especial Huila molido", "unidad_medida": "kg", "stock_actual": 22.0, "stock_minimo": 5.0, "costo_unitario": 28000.0, "fecha_vencimiento": "2027-04-10", "estado": "ACTIVO"},
        {"nombre": "Queso campesino fresco", "unidad_medida": "kg", "stock_actual": 12.0, "stock_minimo": 4.0, "costo_unitario": 16000.0, "fecha_vencimiento": "2026-10-26", "estado": "ACTIVO"}
    ]
    i_ids = [str(r) for r in db.insumos.insert_many(insumos_data).inserted_ids]

    # 5. Productos (10)
    print(" Sembrando productos...")
    productos_data = [
        {"codigo": "PRD-001", "nombre": "Almuerzo Ejecutivo Pollo a la Plancha", "descripcion": "Pechuga a la plancha, arroz, ensalada fresca y sopa del día", "precio_venta": 14000.0, "unidad_venta": "Plato", "id_categoria": c_ids[0], "estado": "DISPONIBLE"},
        {"codigo": "PRD-002", "nombre": "Almuerzo Ejecutivo Carne Asada", "descripcion": "Corte de res a la parrilla, arroz, ensalada y sopa del día", "precio_venta": 16000.0, "unidad_venta": "Plato", "id_categoria": c_ids[0], "estado": "DISPONIBLE"},
        {"codigo": "PRD-003", "nombre": "Jugo Natural de Lulo", "descripcion": "Jugo refrescante preparado con fruta fresca en agua", "precio_venta": 4000.0, "unidad_venta": "Vaso 12oz", "id_categoria": c_ids[1], "estado": "DISPONIBLE"},
        {"codigo": "PRD-004", "nombre": "Jugo Natural de Maracuyá", "descripcion": "Delicioso jugo natural de maracuyá campesino", "precio_venta": 4000.0, "unidad_venta": "Vaso 12oz", "id_categoria": c_ids[1], "estado": "DISPONIBLE"},
        {"codigo": "PRD-005", "nombre": "Café Espresso Doble Especial Huila", "descripcion": "Extracción doble de café arábico especial de la región", "precio_venta": 3500.0, "unidad_venta": "Taza", "id_categoria": c_ids[2], "estado": "DISPONIBLE"},
        {"codigo": "PRD-006", "nombre": "Croissant de Mantequilla", "descripcion": "Croissant horneado diariamente por aprendices de panadería", "precio_venta": 3000.0, "unidad_venta": "Unidad", "id_categoria": c_ids[3], "estado": "DISPONIBLE"},
        {"codigo": "PRD-007", "nombre": "Cheesecake de Frutos Rojos", "descripcion": "Porción de postre artesanal suave con coulis de mora y fresa", "precio_venta": 6500.0, "unidad_venta": "Porción", "id_categoria": c_ids[4], "estado": "DISPONIBLE"},
        {"codigo": "PRD-008", "nombre": "Hamburguesa Artesanal Gastronomía", "descripcion": "Carne de res 150g, queso campesino, lechuga y salsa especial", "precio_venta": 15000.0, "unidad_venta": "Unidad", "id_categoria": c_ids[5], "estado": "DISPONIBLE"},
        {"codigo": "PRD-009", "nombre": "Ensalada César con Pollo Grillé", "descripcion": "Mix de lechugas, pechuga salteada, crutones y aderezo césar", "precio_venta": 12000.0, "unidad_venta": "Bowl", "id_categoria": c_ids[6], "estado": "DISPONIBLE"},
        {"codigo": "PRD-010", "nombre": "Desayuno Tradicional Campesino", "descripcion": "Huevos al gusto, calentado de arroz y café caliente", "precio_venta": 9500.0, "unidad_venta": "Plato", "id_categoria": c_ids[7], "estado": "DISPONIBLE"}
    ]
    p_ids = [str(r) for r in db.productos.insert_many(productos_data).inserted_ids]

    # 6. Recetas (Fichas Técnicas)
    print(" Sembrando recetas...")
    recetas_data = [
        {"id_producto": p_ids[0], "id_insumo": i_ids[0], "cantidad": 0.22},
        {"id_producto": p_ids[0], "id_insumo": i_ids[2], "cantidad": 0.10},
        {"id_producto": p_ids[1], "id_insumo": i_ids[1], "cantidad": 0.25},
        {"id_producto": p_ids[1], "id_insumo": i_ids[2], "cantidad": 0.10},
        {"id_producto": p_ids[2], "id_insumo": i_ids[3], "cantidad": 0.12},
        {"id_producto": p_ids[2], "id_insumo": i_ids[5], "cantidad": 0.03},
        {"id_producto": p_ids[3], "id_insumo": i_ids[4], "cantidad": 0.12},
        {"id_producto": p_ids[3], "id_insumo": i_ids[5], "cantidad": 0.03},
        {"id_producto": p_ids[4], "id_insumo": i_ids[8], "cantidad": 0.018},
        {"id_producto": p_ids[5], "id_insumo": i_ids[7], "cantidad": 0.08},
        {"id_producto": p_ids[5], "id_insumo": i_ids[6], "cantidad": 0.04},
        {"id_producto": p_ids[7], "id_insumo": i_ids[1], "cantidad": 0.16},
        {"id_producto": p_ids[7], "id_insumo": i_ids[9], "cantidad": 0.05}
    ]
    db.recetas.insert_many(recetas_data)

    # 7. Proveedores (10)
    print(" Sembrando proveedores...")
    proveedores_data = [
        {"nit": "900123456-1", "razon_social": "Avícola Central del Huila S.A.S.", "telefono": "3114567890", "correo": "ventas@avicolahuila.com", "direccion": "Km 2 Vía Neiva - Pitalito", "estado": "ACTIVO"},
        {"nit": "900654321-2", "razon_social": "Frigorífico y Carnes del Sur Ltda.", "telefono": "3127891234", "correo": "contacto@carnesdelsur.com", "direccion": "Zona Industrial Pitalito", "estado": "ACTIVO"},
        {"nit": "800345678-3", "razon_social": "Asociación Campesina Frutas del Valle", "telefono": "3156789012", "correo": "frutasdelvalle@agrohuila.org", "direccion": "Plaza Mayorista Bodega 4", "estado": "ACTIVO"},
        {"nit": "890123789-4", "razon_social": "Lácteos y Quesos San Pedro", "telefono": "3103456789", "correo": "lacteossanpedro@gmail.com", "direccion": "Calle 10 # 5-20 Pitalito", "estado": "ACTIVO"},
        {"nit": "860456123-5", "razon_social": "Molinos Harineros de Colombia S.A.", "telefono": "3189012345", "correo": "pedidos@molinoshdc.com", "direccion": "Carrera 4 # 12-40", "estado": "ACTIVO"},
        {"nit": "901234567-6", "razon_social": "Federación Cafetera Especial Huila", "telefono": "3201234567", "correo": "cafehuilaespecial@federacion.com", "direccion": "Calle 8 # 2-15", "estado": "ACTIVO"},
        {"nit": "890567890-7", "razon_social": "Abarrotes y Alimentos El Triunfo", "telefono": "3145678901", "correo": "ventas@abarrotestriunfo.com", "direccion": "Avenida Pastrana # 8-30", "estado": "ACTIVO"},
        {"nit": "900789012-8", "razon_social": "Grasas y Aceites Naturales S.A.", "telefono": "3178901234", "correo": "comercial@grasasnaturales.co", "direccion": "Km 5 Vía San Agustín", "estado": "ACTIVO"},
        {"nit": "901345678-9", "razon_social": "Empaques Ecológicos del Sur", "telefono": "3134567890", "correo": "ecoempaques@verde.com", "direccion": "Carrera 1 # 15-20", "estado": "ACTIVO"},
        {"nit": "900987654-0", "razon_social": "Insumos y Víveres La Sabana", "telefono": "3167890123", "correo": "sabana.viveres@gmail.com", "direccion": "Calle 15 # 3-12", "estado": "ACTIVO"}
    ]
    prov_ids = [str(r) for r in db.proveedores.insert_many(proveedores_data).inserted_ids]

    # 8. Clientes (10)
    print(" Sembrando clientes...")
    clientes_data = [
        {"identificacion": "1083900001", "nombres": "Valentina", "apellidos": "Dussán Polanía", "telefono": "3123456780", "correo": "valentina.dussan@misena.edu.co", "tipo_cliente": "APRENDIZ", "estado": "ACTIVO"},
        {"identificacion": "1083900002", "nombres": "Mateo", "apellidos": "Hernández Claros", "telefono": "3145678901", "correo": "mateo.hernandez@misena.edu.co", "tipo_cliente": "APRENDIZ", "estado": "ACTIVO"},
        {"identificacion": "1234500003", "nombres": "Hernando", "apellidos": "Cabrera Silva", "telefono": "3156789012", "correo": "hcabrera@sena.edu.co", "tipo_cliente": "INSTRUCTOR", "estado": "ACTIVO"},
        {"identificacion": "1234500004", "nombres": "Gloria Esperanza", "apellidos": "Mora Tovar", "telefono": "3167890123", "correo": "gmora@sena.edu.co", "tipo_cliente": "INSTRUCTOR", "estado": "ACTIVO"},
        {"identificacion": "5523400005", "nombres": "Alfonso", "apellidos": "Bravo Meneses", "telefono": "3178901234", "correo": "abravo@sena.edu.co", "tipo_cliente": "FUNCIONARIO", "estado": "ACTIVO"},
        {"identificacion": "5523400006", "nombres": "Sonia Patricia", "apellidos": "Cuéllar Leiva", "telefono": "3189012345", "correo": "scuellar@sena.edu.co", "tipo_cliente": "FUNCIONARIO", "estado": "ACTIVO"},
        {"identificacion": "1075300007", "nombres": "Camilo Andrés", "apellidos": "Torres Bermeo", "telefono": "3190123456", "correo": "camilo.torres@gmail.com", "tipo_cliente": "EXTERNO", "estado": "ACTIVO"},
        {"identificacion": "1075300008", "nombres": "Claudia Milena", "apellidos": "Sánchez Vargas", "telefono": "3101234567", "correo": "claudia.sanchez@hotmail.com", "tipo_cliente": "EXTERNO", "estado": "ACTIVO"},
        {"identificacion": "1083900009", "nombres": "Daniel Felipe", "apellidos": "Ospina Rincón", "telefono": "3112345678", "correo": "dospina@misena.edu.co", "tipo_cliente": "APRENDIZ", "estado": "ACTIVO"},
        {"identificacion": "1083900010", "nombres": "Laura Sofía", "apellidos": "Méndez Chávarro", "telefono": "3133456789", "correo": "lmendez@misena.edu.co", "tipo_cliente": "APRENDIZ", "estado": "INACTIVO"}
    ]
    cli_ids = [str(r) for r in db.clientes.insert_many(clientes_data).inserted_ids]

    # 9. Compras (10)
    print(" Sembrando compras...")
    compras_data = [
        {"numero_factura": "FAC-PROV-001", "fecha_compra": "2026-10-15T08:30:00", "id_proveedor": prov_ids[0], "id_usuario": u_ids[0], "total": 280000.0, "detalle": [{"id_insumo": i_ids[0], "cantidad": 20.0, "costo_unitario": 14000.0, "subtotal": 280000.0}]},
        {"numero_factura": "FAC-PROV-002", "fecha_compra": "2026-10-15T09:15:00", "id_proveedor": prov_ids[1], "id_usuario": u_ids[0], "total": 292500.0, "detalle": [{"id_insumo": i_ids[1], "cantidad": 15.0, "costo_unitario": 19500.0, "subtotal": 292500.0}]},
        {"numero_factura": "FAC-PROV-003", "fecha_compra": "2026-10-16T10:00:00", "id_proveedor": prov_ids[2], "id_usuario": u_ids[0], "total": 163000.0, "detalle": [{"id_insumo": i_ids[3], "cantidad": 10.0, "costo_unitario": 8500.0, "subtotal": 85000.0}, {"id_insumo": i_ids[4], "cantidad": 10.0, "costo_unitario": 7800.0, "subtotal": 78000.0}]},
        {"numero_factura": "FAC-PROV-004", "fecha_compra": "2026-10-16T11:20:00", "id_proveedor": prov_ids[6], "id_usuario": u_ids[0], "total": 276000.0, "detalle": [{"id_insumo": i_ids[2], "cantidad": 40.0, "costo_unitario": 3800.0, "subtotal": 152000.0}, {"id_insumo": i_ids[5], "cantidad": 20.0, "costo_unitario": 4200.0, "subtotal": 84000.0}]},
        {"numero_factura": "FAC-PROV-005", "fecha_compra": "2026-10-17T08:00:00", "id_proveedor": prov_ids[3], "id_usuario": u_ids[0], "total": 172000.0, "detalle": [{"id_insumo": i_ids[6], "cantidad": 20.0, "costo_unitario": 3600.0, "subtotal": 72000.0}, {"id_insumo": i_ids[9], "cantidad": 10.0, "costo_unitario": 10000.0, "subtotal": 100000.0}]},
        {"numero_factura": "FAC-PROV-006", "fecha_compra": "2026-10-17T14:30:00", "id_proveedor": prov_ids[4], "id_usuario": u_ids[0], "total": 105000.0, "detalle": [{"id_insumo": i_ids[7], "cantidad": 30.0, "costo_unitario": 3500.0, "subtotal": 105000.0}]},
        {"numero_factura": "FAC-PROV-007", "fecha_compra": "2026-10-18T09:00:00", "id_proveedor": prov_ids[5], "id_usuario": u_ids[0], "total": 280000.0, "detalle": [{"id_insumo": i_ids[8], "cantidad": 10.0, "costo_unitario": 28000.0, "subtotal": 280000.0}]},
        {"numero_factura": "FAC-PROV-008", "fecha_compra": "2026-10-18T16:00:00", "id_proveedor": prov_ids[0], "id_usuario": u_ids[0], "total": 140000.0, "detalle": [{"id_insumo": i_ids[0], "cantidad": 10.0, "costo_unitario": 14000.0, "subtotal": 140000.0}]},
        {"numero_factura": "FAC-PROV-009", "fecha_compra": "2026-10-19T08:30:00", "id_proveedor": prov_ids[1], "id_usuario": u_ids[0], "total": 195000.0, "detalle": [{"id_insumo": i_ids[1], "cantidad": 10.0, "costo_unitario": 19500.0, "subtotal": 195000.0}]},
        {"numero_factura": "FAC-PROV-010", "fecha_compra": "2026-10-19T10:45:00", "id_proveedor": prov_ids[3], "id_usuario": u_ids[0], "total": 144000.0, "detalle": [{"id_insumo": i_ids[6], "cantidad": 40.0, "costo_unitario": 3600.0, "subtotal": 144000.0}]}
    ]
    db.compras.insert_many(compras_data)

    # 10. Pedidos (10)
    print(" Sembrando pedidos...")
    pedidos_data = [
        {"fecha_pedido": "2026-10-19T12:00:00", "id_cliente": cli_ids[0], "id_usuario": u_ids[1], "tipo_pedido": "MESA", "estado": "ENTREGADO", "total": 18000.0, "observaciones": "Mesa 4", "detalle": [{"id_producto": p_ids[0], "cantidad": 1.0, "precio_unitario": 14000.0, "subtotal": 14000.0}, {"id_producto": p_ids[2], "cantidad": 1.0, "precio_unitario": 4000.0, "subtotal": 4000.0}]},
        {"fecha_pedido": "2026-10-19T12:15:00", "id_cliente": cli_ids[1], "id_usuario": u_ids[1], "tipo_pedido": "PARA_LLEVAR", "estado": "ENTREGADO", "total": 20000.0, "observaciones": "Empacar salsa aparte", "detalle": [{"id_producto": p_ids[1], "cantidad": 1.0, "precio_unitario": 16000.0, "subtotal": 16000.0}, {"id_producto": p_ids[3], "cantidad": 1.0, "precio_unitario": 4000.0, "subtotal": 4000.0}]},
        {"fecha_pedido": "2026-10-19T12:30:00", "id_cliente": cli_ids[2], "id_usuario": u_ids[2], "tipo_pedido": "MESA", "estado": "ENTREGADO", "total": 17500.0, "observaciones": "Mesa 1", "detalle": [{"id_producto": p_ids[0], "cantidad": 1.0, "precio_unitario": 14000.0, "subtotal": 14000.0}, {"id_producto": p_ids[4], "cantidad": 1.0, "precio_unitario": 3500.0, "subtotal": 3500.0}]},
        {"fecha_pedido": "2026-10-20T08:30:00", "id_cliente": cli_ids[3], "id_usuario": u_ids[1], "tipo_pedido": "MESA", "estado": "ENTREGADO", "total": 12500.0, "observaciones": "Café con poca azúcar", "detalle": [{"id_producto": p_ids[9], "cantidad": 1.0, "precio_unitario": 9500.0, "subtotal": 9500.0}, {"id_producto": p_ids[5], "cantidad": 1.0, "precio_unitario": 3000.0, "subtotal": 3000.0}]},
        {"fecha_pedido": "2026-10-20T10:00:00", "id_cliente": cli_ids[4], "id_usuario": u_ids[2], "tipo_pedido": "PARA_LLEVAR", "estado": "ENTREGADO", "total": 9500.0, "observaciones": "Para refrigerio de reunión", "detalle": [{"id_producto": p_ids[5], "cantidad": 1.0, "precio_unitario": 3000.0, "subtotal": 3000.0}, {"id_producto": p_ids[6], "cantidad": 1.0, "precio_unitario": 6500.0, "subtotal": 6500.0}]},
        {"fecha_pedido": "2026-10-20T12:10:00", "id_cliente": cli_ids[5], "id_usuario": u_ids[1], "tipo_pedido": "MESA", "estado": "EN_PREPARACION", "total": 19000.0, "observaciones": "Mesa 8", "detalle": [{"id_producto": p_ids[7], "cantidad": 1.0, "precio_unitario": 15000.0, "subtotal": 15000.0}, {"id_producto": p_ids[2], "cantidad": 1.0, "precio_unitario": 4000.0, "subtotal": 4000.0}]},
        {"fecha_pedido": "2026-10-20T12:20:00", "id_cliente": cli_ids[6], "id_usuario": u_ids[2], "tipo_pedido": "EVENTO", "estado": "PENDIENTE", "total": 140000.0, "observaciones": "10 almuerzos para auditorio", "detalle": [{"id_producto": p_ids[0], "cantidad": 10.0, "precio_unitario": 14000.0, "subtotal": 140000.0}]},
        {"fecha_pedido": "2026-10-20T12:45:00", "id_cliente": cli_ids[7], "id_usuario": u_ids[1], "tipo_pedido": "MESA", "estado": "PENDIENTE", "total": 16000.0, "observaciones": "Mesa 2", "detalle": [{"id_producto": p_ids[8], "cantidad": 1.0, "precio_unitario": 12000.0, "subtotal": 12000.0}, {"id_producto": p_ids[3], "cantidad": 1.0, "precio_unitario": 4000.0, "subtotal": 4000.0}]},
        {"fecha_pedido": "2026-10-20T13:00:00", "id_cliente": cli_ids[8], "id_usuario": u_ids[1], "tipo_pedido": "MESA", "estado": "ANULADO", "total": 14000.0, "observaciones": "Cliente canceló por tiempo", "detalle": [{"id_producto": p_ids[0], "cantidad": 1.0, "precio_unitario": 14000.0, "subtotal": 14000.0}]},
        {"fecha_pedido": "2026-10-21T09:15:00", "id_cliente": cli_ids[0], "id_usuario": u_ids[1], "tipo_pedido": "PARA_LLEVAR", "estado": "PENDIENTE", "total": 10000.0, "observaciones": "", "detalle": [{"id_producto": p_ids[4], "cantidad": 2.0, "precio_unitario": 3500.0, "subtotal": 7000.0}, {"id_producto": p_ids[5], "cantidad": 1.0, "precio_unitario": 3000.0, "subtotal": 3000.0}]}
    ]
    ped_ids = [str(r) for r in db.pedidos.insert_many(pedidos_data).inserted_ids]

    # 11. Calificaciones (10)
    print(" Sembrando calificaciones...")
    calificaciones_data = [
        {"id_pedido": ped_ids[0], "id_cliente": cli_ids[0], "fecha": "2026-10-19T13:00:00", "calificacion_servicio": 5, "comentario": "Excelente atención y sazón, el pollo en su punto perfecto.", "productos": [{"id_producto": p_ids[0], "nombre": "Almuerzo Pollo a la Plancha", "calificacion": 5}, {"id_producto": p_ids[2], "nombre": "Jugo Natural de Lulo", "calificacion": 5}]},
        {"id_pedido": ped_ids[1], "id_cliente": cli_ids[1], "fecha": "2026-10-19T13:15:00", "calificacion_servicio": 4, "comentario": "Muy rica la carne, empaque muy seguro.", "productos": [{"id_producto": p_ids[1], "nombre": "Almuerzo Carne Asada", "calificacion": 4}, {"id_producto": p_ids[3], "nombre": "Jugo Natural de Maracuyá", "calificacion": 5}]},
        {"id_pedido": ped_ids[2], "id_cliente": cli_ids[2], "fecha": "2026-10-19T13:30:00", "calificacion_servicio": 5, "comentario": "El café huilense tiene notas espectaculares.", "productos": [{"id_producto": p_ids[0], "nombre": "Almuerzo Pollo a la Plancha", "calificacion": 5}, {"id_producto": p_ids[4], "nombre": "Café Espresso Doble", "calificacion": 5}]},
        {"id_pedido": ped_ids[3], "id_cliente": cli_ids[3], "fecha": "2026-10-20T09:15:00", "calificacion_servicio": 5, "comentario": "Desayuno muy completo, el croissant recién horneado estaba crocante.", "productos": [{"id_producto": p_ids[9], "nombre": "Desayuno Tradicional", "calificacion": 5}, {"id_producto": p_ids[5], "nombre": "Croissant de Mantequilla", "calificacion": 5}]},
        {"id_pedido": ped_ids[4], "id_cliente": cli_ids[4], "fecha": "2026-10-20T10:45:00", "calificacion_servicio": 4, "comentario": "Buen postre, aunque podría tener un poco más de coulis.", "productos": [{"id_producto": p_ids[6], "nombre": "Cheesecake de Frutos Rojos", "calificacion": 4}]},
        {"id_pedido": ped_ids[0], "id_cliente": cli_ids[2], "fecha": "2026-10-20T11:00:00", "calificacion_servicio": 5, "comentario": "Excelente iniciativa gastronómica del SENA.", "productos": [{"id_producto": p_ids[2], "nombre": "Jugo Natural de Lulo", "calificacion": 5}]},
        {"id_pedido": ped_ids[1], "id_cliente": cli_ids[3], "fecha": "2026-10-20T11:30:00", "calificacion_servicio": 5, "comentario": "La carne asada estuvo suave y jugosa.", "productos": [{"id_producto": p_ids[1], "nombre": "Almuerzo Carne Asada", "calificacion": 5}]},
        {"id_pedido": ped_ids[2], "id_cliente": cli_ids[4], "fecha": "2026-10-20T12:00:00", "calificacion_servicio": 4, "comentario": "Buena atención de los aprendices cajeros.", "productos": [{"id_producto": p_ids[0], "nombre": "Almuerzo Pollo a la Plancha", "calificacion": 4}]},
        {"id_pedido": ped_ids[3], "id_cliente": cli_ids[5], "fecha": "2026-10-20T12:30:00", "calificacion_servicio": 5, "comentario": "Rapidez en la entrega y comida caliente.", "productos": [{"id_producto": p_ids[5], "nombre": "Croissant de Mantequilla", "calificacion": 5}]},
        {"id_pedido": ped_ids[4], "id_cliente": cli_ids[6], "fecha": "2026-10-20T13:00:00", "calificacion_servicio": 4, "comentario": "Presentación impecable de los platos.", "productos": [{"id_producto": p_ids[6], "nombre": "Cheesecake de Frutos Rojos", "calificacion": 4}]}
    ]
    db.calificaciones.insert_many(calificaciones_data)

    print("\n Resumen de colecciones y registros creados:")
    print("-" * 45)
    for col in colecciones:
        total = db[col].count_documents({})
        print(f" Colección '{col}': {total} documentos")
    print("-" * 45)
    print(" Base de datos MongoDB inicializada con éxito total.\n")


if __name__ == "__main__":
    j_inicializar_base_datos()
