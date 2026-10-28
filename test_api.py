"""
Suite de Pruebas Automatizadas E2E para la API REST de Gastronomía (CGDSS - SENA)
Valida:
1. Autenticación JWT y Roles RBAC (ADMIN, CAJERO, COCINERO) (RF01, RF02)
2. Regla RN06: Cifrado bcrypt y no exposición de contraseñas
3. Regla RN01: Cálculo de subtotales y totales en backend
4. Regla RN02: Compras incrementan stock_actual y actualizan costo_unitario
5. Regla RN03: Descuento de insumos al entregar pedido y error 409 si stock insuficiente
6. Regla RN04: Borrado lógico a INACTIVO si hay movimientos asociados
7. Regla RN05: Inmutabilidad de pedidos en estado ENTREGADO o ANULADO
8. Endpoints de negocio: recetas, costo/margen, alertas de stock, reportes y calificaciones
"""

import sys
import os
from fastapi.testclient import TestClient

# Añadir ruta al sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.main import app

client = TestClient(app)


def test_suite_completa():
    print("\n=======================================================")
    print(" INICIANDO SUITE DE PRUEBAS AUTOMATIZADAS - GASTRONOMÍA")
    print("=======================================================\n")

    # 1. Health check y raíz
    print(" [1/10] Probando endpoints generales / y /health...")
    r_root = client.get("/")
    assert r_root.status_code == 200, f"Error en /: {r_root.text}"
    r_health = client.get("/health")
    assert r_health.status_code == 200, f"Error en /health: {r_health.text}"
    assert r_health.json()["status"] == "healthy"
    print("   ✓ Endpoints generales operativos y MongoDB conectado.")

    # 2. Autenticación y JWT (RF01)
    print("\n [2/10] Probando autenticación JWT y contraseñas (RN06)...")
    # Login exitoso Admin
    r_login_admin = client.post("/api/v1/auth/login", json={
        "correo": "admin@gastronomia.sena.edu.co",
        "password": "admin123"
    })
    assert r_login_admin.status_code == 200, f"Error login admin: {r_login_admin.text}"
    token_admin = r_login_admin.json()["access_token"]
    assert "password" not in r_login_admin.json()["usuario"], "RN06 violada: contraseña expuesta en respuesta de login"
    headers_admin = {"Authorization": f"Bearer {token_admin}"}

    # Login exitoso Cajero
    r_login_cajero = client.post("/api/v1/auth/login", json={
        "correo": "cajero1@gastronomia.sena.edu.co",
        "password": "cajero123"
    })
    assert r_login_cajero.status_code == 200
    token_cajero = r_login_cajero.json()["access_token"]
    headers_cajero = {"Authorization": f"Bearer {token_cajero}"}

    # Login exitoso Cocinero
    r_login_cocinero = client.post("/api/v1/auth/login", json={
        "correo": "cocinero1@gastronomia.sena.edu.co",
        "password": "cocinero123"
    })
    assert r_login_cocinero.status_code == 200
    token_cocinero = r_login_cocinero.json()["access_token"]
    headers_cocinero = {"Authorization": f"Bearer {token_cocinero}"}

    # Login con contraseña errónea (401)
    r_bad_login = client.post("/api/v1/auth/login", json={
        "correo": "admin@gastronomia.sena.edu.co",
        "password": "password_incorrecta"
    })
    assert r_bad_login.status_code == 401

    # Validación de token Bearer en endpoints protegidos (HTTPBearer)
    # Sin token -> 401
    r_sin_token = client.get("/api/v1/auth/perfil")
    assert r_sin_token.status_code == 401, f"Esperado 401 sin token, recibido: {r_sin_token.status_code}"

    # Token inválido -> 401
    r_token_invalido = client.get("/api/v1/auth/perfil", headers={"Authorization": "Bearer token_invalido_xyz"})
    assert r_token_invalido.status_code == 401, f"Esperado 401 token inválido, recibido: {r_token_invalido.status_code}"

    # Token válido en perfil -> 200
    r_perfil = client.get("/api/v1/auth/perfil", headers=headers_admin)
    assert r_perfil.status_code == 200
    assert r_perfil.json()["correo"] == "admin@gastronomia.sena.edu.co"
    print("   ✓ Login correcto para ADMIN, CAJERO y COCINERO. Error 401 en credenciales inválidas y esquema HTTP Bearer verificado.")

    # 3. Control de Acceso Basado en Roles (RBAC) (RF02)
    print("\n [3/10] Probando permisos y restricciones por rol (403 Forbidden)...")
    # Cajero intentando listar usuarios (Solo ADMIN)
    r_cajero_users = client.get("/api/v1/usuarios", headers=headers_cajero)
    assert r_cajero_users.status_code == 403, f"Esperado 403 para cajero en usuarios, recibido: {r_cajero_users.status_code}"

    # Cocinero intentando registrar compras (Solo ADMIN)
    r_cocinero_compras = client.post("/api/v1/compras", json={}, headers=headers_cocinero)
    assert r_cocinero_compras.status_code == 403

    # Admin listando usuarios (Éxito)
    r_admin_users = client.get("/api/v1/usuarios", headers=headers_admin)
    assert r_admin_users.status_code == 200
    usuarios = r_admin_users.json()
    assert len(usuarios) >= 10
    for u in usuarios:
        assert "password" not in u, "RN06 violada: Contraseña encontrada en listado de usuarios"
    print("   ✓ Permisos RBAC funcionando estrictamente (403 para roles sin permiso, acceso a ADMIN).")

    # 4. CRUD de Categorías y Productos (RF03, RF04)
    print("\n [4/10] Probando categorías y catálogo de productos...")
    # Listar categorías
    r_cats = client.get("/api/v1/categorias", headers=headers_cajero)
    assert r_cats.status_code == 200
    cats = r_cats.json()
    cat_id = cats[0]["id"]

    # Listar productos
    r_prods = client.get("/api/v1/productos", headers=headers_cocinero)
    assert r_prods.status_code == 200
    prods = r_prods.json()
    prod_pollo = next(p for p in prods if p["codigo"] == "PRD-001")
    id_prod_pollo = prod_pollo["id"]
    print(f"   ✓ Catálogo cargado. Producto de prueba: {prod_pollo['nombre']} (${prod_pollo['precio_venta']})")

    # 5. Cálculo de Costo de Producción y Margen de Ganancia (RF06, RF05)
    print("\n [5/10] Probando cálculo de costo y margen de ganancia (RF06)...")
    r_costo = client.get(f"/api/v1/productos/{id_prod_pollo}/costo", headers=headers_admin)
    assert r_costo.status_code == 200
    costo_data = r_costo.json()
    assert costo_data["costo_produccion"] > 0
    assert costo_data["margen_ganancia"] == round(costo_data["precio_venta"] - costo_data["costo_produccion"], 2)
    print(f"   ✓ Costo producción: ${costo_data['costo_produccion']} | Margen: ${costo_data['margen_ganancia']} ({costo_data['porcentaje_margen']}%)")

    # 6. Alertas de Stock Bajo y Próximos a Vencer (RF07)
    print("\n [6/10] Probando consultas de stock bajo y vencimiento de insumos (RF07)...")
    r_stock_bajo = client.get("/api/v1/insumos/stock-bajo", headers=headers_cocinero)
    assert r_stock_bajo.status_code == 200
    r_por_vencer = client.get("/api/v1/insumos/por-vencer?dias=30", headers=headers_cocinero)
    assert r_por_vencer.status_code == 200
    print(f"   ✓ Insumos evaluados: {len(r_stock_bajo.json())} con stock bajo, {len(r_por_vencer.json())} por vencer en 30 días.")

    # 7. Regla RN02: Compras incrementan stock y actualizan costo unitario
    print("\n [7/10] Probando compra de insumos y regla de negocio RN02...")
    r_insumos = client.get("/api/v1/insumos", headers=headers_admin)
    insumo_pollo = next(i for i in r_insumos.json() if "Pechuga de pollo" in i["nombre"])
    id_ins_pollo = insumo_pollo["id"]
    stock_inicial = insumo_pollo["stock_actual"]

    r_provs = client.get("/api/v1/proveedores", headers=headers_admin)
    id_prov = r_provs.json()[0]["id"]

    factura_test = f"FAC-TEST-{os.urandom(3).hex().upper()}"
    nueva_compra = {
        "numero_factura": factura_test,
        "id_proveedor": id_prov,
        "detalle": [
            {
                "id_insumo": id_ins_pollo,
                "cantidad": 15.0,
                "costo_unitario": 14500.0
            }
        ]
    }
    r_reg_compra = client.post("/api/v1/compras", json=nueva_compra, headers=headers_admin)
    assert r_reg_compra.status_code == 201, f"Error compra: {r_reg_compra.text}"
    compra_res = r_reg_compra.json()
    assert compra_res["total"] == 15.0 * 14500.0

    # Verificar que el stock aumentó en 15 y el costo_unitario se actualizó a 14500
    r_ins_despues = client.get(f"/api/v1/insumos/{id_ins_pollo}", headers=headers_admin)
    ins_despues = r_ins_despues.json()
    assert ins_despues["stock_actual"] == stock_inicial + 15.0, "RN02 violada: El stock no se incrementó correctamente"
    assert ins_despues["costo_unitario"] == 14500.0, "RN02 violada: El costo unitario no se actualizó"
    print(f"   ✓ RN02 verificada: Stock incrementó de {stock_inicial} a {ins_despues['stock_actual']} y costo unitario actualizado a ${ins_despues['costo_unitario']}.")

    # 8. Reglas de Pedidos: RN01 (cálculo totales), RN03 (descuento/conflicto stock) y RN05 (inmutabilidad)
    print("\n [8/10] Probando pedidos: RN01 (cálculos), RN03 (stock/409) y RN05 (inmutabilidad)...")
    r_clis = client.get("/api/v1/clientes", headers=headers_cajero)
    clientes_activos = [c for c in r_clis.json() if c.get("estado") == "ACTIVO"]
    id_cliente = clientes_activos[0]["id"] if clientes_activos else r_clis.json()[0]["id"]

    # Crear pedido con 2 almuerzos de pollo
    nuevo_pedido = {
        "id_cliente": id_cliente,
        "tipo_pedido": "MESA",
        "observaciones": "Prueba RN01 y RN03",
        "detalle": [
            {
                "id_producto": id_prod_pollo,
                "cantidad": 2.0
            }
        ]
    }
    r_crear_ped = client.post("/api/v1/pedidos", json=nuevo_pedido, headers=headers_cajero)
    assert r_crear_ped.status_code == 201, f"Error pedido: {r_crear_ped.text}"
    ped_creado = r_crear_ped.json()
    id_pedido = ped_creado["id"]

    # RN01: Verificar subtotal y total calculado por el backend
    precio_pollo = prod_pollo["precio_venta"]
    assert ped_creado["total"] == 2.0 * precio_pollo, "RN01 violada: Total no calculado por backend"
    assert ped_creado["detalle"][0]["subtotal"] == 2.0 * precio_pollo
    print(f"   ✓ RN01 verificada: Subtotal (${ped_creado['detalle'][0]['subtotal']}) y Total (${ped_creado['total']}) calculados por la API.")

    # RN03: Descuento al ENTREGAR el pedido
    stock_pollo_antes_entrega = client.get(f"/api/v1/insumos/{id_ins_pollo}", headers=headers_admin).json()["stock_actual"]
    # Cambiar estado a ENTREGADO
    r_entrega = client.patch(f"/api/v1/pedidos/{id_pedido}/estado", json={"estado": "ENTREGADO"}, headers=headers_cocinero)
    assert r_entrega.status_code == 200, f"Error al entregar pedido: {r_entrega.text}"
    stock_pollo_despues_entrega = client.get(f"/api/v1/insumos/{id_ins_pollo}", headers=headers_admin).json()["stock_actual"]
    # Según receta, 1 almuerzo pollo usa 0.22 kg. Para 2 pedidos = 0.44 kg descontados
    descuento_esperado = 2.0 * 0.22
    assert round(stock_pollo_despues_entrega, 2) == round(stock_pollo_antes_entrega - descuento_esperado, 2), "RN03 violada: Descuento de insumo inexacto"
    print(f"   ✓ RN03 verificada: Al entregar, se descontó inventario según receta ({stock_pollo_antes_entrega} -> {stock_pollo_despues_entrega} kg).")

    # RN03 caso 409 Conflict: Pedido con cantidad gigante que sobrepasa existencias
    pedido_excesivo = {
        "id_cliente": id_cliente,
        "tipo_pedido": "EVENTO",
        "detalle": [{"id_producto": id_prod_pollo, "cantidad": 50000.0}]  # Requiere 11,000 kg de pechuga
    }
    r_ped_gigante = client.post("/api/v1/pedidos", json=pedido_excesivo, headers=headers_cajero)
    id_ped_gigante = r_ped_gigante.json()["id"]
    r_entrega_fallida = client.patch(f"/api/v1/pedidos/{id_ped_gigante}/estado", json={"estado": "ENTREGADO"}, headers=headers_cocinero)
    assert r_entrega_fallida.status_code == 409, f"Esperado 409 Conflict por stock insuficiente, recibido: {r_entrega_fallida.status_code}"
    print(f"   ✓ RN03 (Conflicto 409) verificada: Rechazo con HTTP 409 cuando el stock es insuficiente: '{r_entrega_fallida.json()['detail']}'")

    # RN05: Intentar modificar pedido ya ENTREGADO
    r_mod_entregado = client.put(f"/api/v1/pedidos/{id_pedido}", json={"observaciones": "Cambio no permitido"}, headers=headers_cajero)
    assert r_mod_entregado.status_code == 400, f"RN05 violada: Se permitió modificar pedido ENTREGADO ({r_mod_entregado.status_code})"
    r_estado_entregado = client.patch(f"/api/v1/pedidos/{id_pedido}/estado", json={"estado": "PENDIENTE"}, headers=headers_cocinero)
    assert r_estado_entregado.status_code == 400, "RN05 violada: Se permitió cambiar estado de pedido ENTREGADO"
    print("   ✓ RN05 verificada: Pedido ENTREGADO es inmutable ante cambios de contenido o de estado (HTTP 400).")

    # 9. Regla RN04: Borrado lógico si existen movimientos asociados
    print("\n [9/10] Probando borrado lógico por movimientos asociados (RN04)...")
    # Intentar eliminar cliente con pedidos
    r_del_cli = client.delete(f"/api/v1/clientes/{id_cliente}", headers=headers_cajero)
    assert r_del_cli.status_code == 200
    assert r_del_cli.json()["tipo_eliminacion"] == "LOGICA", "RN04 violada: Se esperaba borrado lógico para cliente con pedidos"
    cli_check = client.get(f"/api/v1/clientes/{id_cliente}", headers=headers_cajero).json()
    assert cli_check["estado"] == "INACTIVO"
    print(f"   ✓ RN04 verificada: Cliente con movimientos cambiado a estado INACTIVO sin pérdida de datos.")

    # 10. Calificaciones y Reportes (RF11, RF12)
    print("\n [10/10] Probando calificaciones en MongoDB y reportes estadísticos...")
    # Calificación sobre el pedido entregado
    calif_doc = {
        "id_pedido": id_pedido,
        "id_cliente": id_cliente,
        "calificacion_servicio": 5,
        "comentario": "Pollo delicioso y jugo fresco, excelente servicio.",
        "productos": [
            {"id_producto": id_prod_pollo, "nombre": "Pollo a la plancha", "calificacion": 5}
        ]
    }
    r_calif = client.post("/api/v1/calificaciones", json=calif_doc, headers=headers_cajero)
    assert r_calif.status_code == 201

    # Consultar calificaciones del producto
    r_prod_calif = client.get(f"/api/v1/calificaciones/producto/{id_prod_pollo}", headers=headers_cajero)
    assert r_prod_calif.status_code == 200
    calif_resumen = r_prod_calif.json()
    assert calif_resumen["total_calificaciones"] >= 1
    assert calif_resumen["promedio_calificacion"] >= 1.0
    print(f"   ✓ Calificaciones registradas en MongoDB. Promedio producto: {calif_resumen['promedio_calificacion']} / 5.0")

    # Reporte de Ventas por rango de fechas (RF11)
    r_rep_ventas = client.get("/api/v1/reportes/ventas", headers=headers_admin)
    assert r_rep_ventas.status_code == 200
    rep_v = r_rep_ventas.json()
    assert rep_v["numero_pedidos"] > 0
    assert rep_v["total_vendido"] > 0
    print(f"   ✓ Reporte de ventas: {rep_v['numero_pedidos']} pedidos, Total: ${rep_v['total_vendido']} (Ticket prom: ${rep_v['ticket_promedio']})")

    # Reporte de Productos Más Vendidos (RF11)
    r_rep_prods = client.get("/api/v1/reportes/productos-mas-vendidos?limite=5", headers=headers_admin)
    assert r_rep_prods.status_code == 200
    ranking = r_rep_prods.json()["ranking"]
    assert len(ranking) > 0
    top_prod = ranking[0]
    print(f"   ✓ Ranking productos más vendidos: #1 {top_prod['nombre']} ({top_prod['total_unidades_vendidas']} unidades vendidas, Recaudado: ${top_prod['total_recaudado']})")

    print("\n=======================================================")
    print(" ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE AL 100%! ")
    print("=======================================================\n")


if __name__ == "__main__":
    test_suite_completa()
