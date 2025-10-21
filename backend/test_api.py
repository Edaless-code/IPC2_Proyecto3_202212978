"""
Script para probar el API Flask - VERSIÓN CORREGIDA
"""
import requests
import json
import os

BASE_URL = 'http://localhost:5000'

def test_inicializar_sistema():
    """Prueba inicialización del sistema"""
    print("\n" + "="*60)
    print("=== Inicializando sistema ===")
    print("="*60)
    response = requests.post(f'{BASE_URL}/inicializarSistema')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_procesar_configuracion():
    """Prueba procesamiento de XML de configuración"""
    print("\n" + "="*60)
    print("=== Procesando configuración ===")
    print("="*60)
    
    if not os.path.exists('ejemplo_configuracion.xml'):
        print("❌ ERROR: No se encuentra ejemplo_configuracion.xml")
        return
    
    with open('ejemplo_configuracion.xml', 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print(f"📤 Enviando {len(xml_content)} caracteres")
    
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    response = requests.post(
        f'{BASE_URL}/procesarConfiguracion',
        data=xml_content.encode('utf-8'),
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result['status'] == 'success':
        stats = result['estadisticas']
        print(f"✅ Recursos creados: {stats['recursos']}")
        print(f"✅ Categorías creadas: {stats['categorias']}")
        print(f"✅ Configuraciones creadas: {stats['configuraciones']}")
        print(f"✅ Clientes creados: {stats['clientes']}")
        print(f"✅ Instancias creadas: {stats['instancias']}")
    else:
        print(f"❌ Error: {result.get('message', 'Error desconocido')}")

def test_procesar_consumos():
    """Prueba procesamiento de XML de consumos"""
    print("\n" + "="*60)
    print("=== Procesando consumos ===")
    print("="*60)
    
    if not os.path.exists('ejemplo_consumos.xml'):
        print("❌ ERROR: No se encuentra ejemplo_consumos.xml")
        return
    
    with open('ejemplo_consumos.xml', 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    print(f"📤 Enviando {len(xml_content)} caracteres")
    
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    response = requests.post(
        f'{BASE_URL}/procesarConsumos',
        data=xml_content.encode('utf-8'),
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result['status'] == 'success':
        print(f"✅ {result['message']}")
        print(f"📊 Consumos procesados: {result['cantidad']}")
    else:
        print(f"❌ Error: {result.get('message', 'Error desconocido')}")

def test_consultar_datos():
    """Prueba consulta de datos"""
    print("\n" + "="*60)
    print("=== Consultando datos del sistema ===")
    print("="*60)
    response = requests.get(f'{BASE_URL}/consultarDatos')
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data['status'] == 'success':
        print(f"📦 Recursos: {len(data['data']['recursos'])}")
        print(f"📁 Categorías: {len(data['data']['categorias'])}")
        print(f"⚙️  Configuraciones: {len(data['data']['configuraciones'])}")
        print(f"👥 Clientes: {len(data['data']['clientes'])}")
        print(f"📄 Facturas: {len(data['data']['facturas'])}")
        
        # Mostrar algunos detalles
        if data['data']['recursos']:
            print("\n📋 Recursos disponibles:")
            for recurso in data['data']['recursos'][:3]:
                print(f"   - {recurso['nombre']} ({recurso['abreviatura']}): ${recurso['valor_x_hora']}/hora")
        
        if data['data']['clientes']:
            print("\n👥 Clientes registrados:")
            for cliente in data['data']['clientes']:
                print(f"   - {cliente['nombre']} (NIT: {cliente['nit']})")
                print(f"     Instancias: {len(cliente['instancias'])}")

def test_crear_recurso():
    """Prueba creación de recurso individual"""
    print("\n" + "="*60)
    print("=== Creando recurso adicional ===")
    print("="*60)
    
    data = {
        'id': 10,
        'nombre': 'Balanceador de Carga',
        'abreviatura': 'LB',
        'metrica': 'unidad',
        'tipo': 'Software',
        'valorXhora': 1.5
    }
    
    response = requests.post(f'{BASE_URL}/crearRecurso', json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result['status'] == 'success':
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")

def test_crear_cliente():
    """Prueba creación de cliente individual"""
    print("\n" + "="*60)
    print("=== Creando cliente adicional ===")
    print("="*60)
    
    data = {
        'nit': '11111111-K',
        'nombre': 'Nuevo Cliente S.A.',
        'usuario': 'nuevo_cliente',
        'clave': 'pass789',
        'direccion': 'Zona 15, Guatemala',
        'correoElectronico': 'nuevo@cliente.com'
    }
    
    response = requests.post(f'{BASE_URL}/crearCliente', json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result['status'] == 'success':
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")

def test_crear_instancia():
    """Prueba creación de instancia"""
    print("\n" + "="*60)
    print("=== Creando instancia adicional ===")
    print("="*60)
    
    data = {
        'nitCliente': '12345678-9',
        'id': 100,
        'idConfiguracion': 1,
        'nombre': 'Nueva Instancia Test',
        'fechaInicio': '25/01/2025',
        'estado': 'Vigente'
    }
    
    response = requests.post(f'{BASE_URL}/crearInstancia', json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result['status'] == 'success':
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")

def test_generar_facturas():
    """Prueba generación de facturas"""
    print("\n" + "="*60)
    print("=== Generando facturas ===")
    print("="*60)
    
    data = {
        'fechaInicio': '01/01/2025',
        'fechaFin': '31/01/2025'
    }
    
    response = requests.post(f'{BASE_URL}/generarFacturas', json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result['status'] == 'success':
        print(f"✅ Facturas generadas: {len(result['facturas'])}")
        for factura in result['facturas']:
            print(f"\n📄 Factura #{factura['numero']}")
            print(f"   Cliente: {factura['nombre_cliente']} (NIT: {factura['nit_cliente']})")
            print(f"   Fecha: {factura['fecha']}")
            print(f"   💰 Total: ${factura['total']:.2f}")
            print(f"   Detalles: {len(factura['detalles'])} instancia(s)")
    else:
        print(f"ℹ️  {result['message']}")

def test_obtener_factura():
    """Prueba obtención de factura específica"""
    print("\n" + "="*60)
    print("=== Obteniendo factura #1 ===")
    print("="*60)
    
    response = requests.get(f'{BASE_URL}/obtenerFactura/1')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        factura = result['factura']
        print(f"\n📄 Factura #{factura['numero']}")
        print(f"Cliente: {factura['nombre_cliente']} (NIT: {factura['nit_cliente']})")
        print(f"Fecha: {factura['fecha']}")
        print(f"💰 Total: ${factura['total']:.2f}")
        print(f"\n📋 Detalles:")
        for detalle in factura['detalles']:
            print(f"  • {detalle['nombre_instancia']}")
            print(f"    Config: {detalle['nombre_configuracion']}")
            print(f"    Horas: {detalle['horas_consumidas']:.2f}h")
            print(f"    Subtotal: ${detalle['subtotal']:.2f}")
    else:
        print("ℹ️  Factura no encontrada (primero genera facturas)")

def test_analizar_ventas_categorias():
    """Prueba análisis de ventas por categorías"""
    print("\n" + "="*60)
    print("=== Análisis de ventas por categorías ===")
    print("="*60)
    
    data = {
        'fechaInicio': '01/01/2025',
        'fechaFin': '31/01/2025'
    }
    
    response = requests.post(f'{BASE_URL}/analizarVentasCategorias', json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result['analisis']:
            print("\n📊 Top configuraciones por ingresos:")
            for i, item in enumerate(result['analisis'][:5], 1):
                print(f"\n{i}. {item['configuracion']}")
                print(f"   Categoría: {item['categoria']}")
                print(f"   💰 Ingresos: ${item['ingresos']:.2f}")
                print(f"   📦 Instancias facturadas: {item['instancias_facturadas']}")
        else:
            print("ℹ️  No hay datos de ventas aún")

def test_analizar_ventas_recursos():
    """Prueba análisis de ventas por recursos"""
    print("\n" + "="*60)
    print("=== Análisis de ventas por recursos ===")
    print("="*60)
    
    data = {
        'fechaInicio': '01/01/2025',
        'fechaFin': '31/01/2025'
    }
    
    response = requests.post(f'{BASE_URL}/analizarVentasRecursos', json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result['analisis']:
            print("\n📊 Top recursos por ingresos:")
            for i, item in enumerate(result['analisis'][:5], 1):
                print(f"\n{i}. {item['recurso']} ({item['abreviatura']})")
                print(f"   Métrica: {item['metrica']}")
                print(f"   💰 Ingresos: ${item['ingresos']:.2f}")
                print(f"   ⏱️  Horas totales: {item['horas_totales']:.2f}h")
        else:
            print("ℹ️  No hay datos de ventas aún")

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*60)
    print("🚀 PRUEBAS DEL API - Tecnologías Chapinas S.A.")
    print("="*60)
    
    try:
        # 1. Inicializar sistema
        test_inicializar_sistema()
        
        # 2. Procesar configuración
        test_procesar_configuracion()
        
        # 3. Procesar consumos
        test_procesar_consumos()
        
        # 4. Consultar datos
        test_consultar_datos()
        
        # 5. Crear recurso individual
        test_crear_recurso()
        
        # 6. Crear cliente individual
        test_crear_cliente()
        
        # 7. Crear instancia
        test_crear_instancia()
        
        # 8. Generar facturas
        test_generar_facturas()
        
        # 9. Obtener factura específica
        test_obtener_factura()
        
        # 10. Análisis de ventas por categorías
        test_analizar_ventas_categorias()
        
        # 11. Análisis de ventas por recursos
        test_analizar_ventas_recursos()
        
        print("\n" + "="*60)
        print("✅ PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ [ERROR] No se pudo conectar al servidor.")
        print("Asegúrate de que el API Flask esté ejecutándose:")
        print("  python app.py")
    except Exception as e:
        print(f"\n❌ [ERROR] {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()