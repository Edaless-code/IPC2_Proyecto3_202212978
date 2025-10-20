"""
Script para probar el API Flask
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_inicializar_sistema():
    """Prueba inicialización del sistema"""
    print("\n=== Inicializando sistema ===")
    response = requests.post(f'{BASE_URL}/inicializarSistema')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_procesar_configuracion():
    """Prueba procesamiento de XML de configuración"""
    print("\n=== Procesando configuración ===")
    
    with open('ejemplo_configuracion.xml', 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(
        f'{BASE_URL}/procesarConfiguracion',
        data=xml_content,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_procesar_consumos():
    """Prueba procesamiento de XML de consumos"""
    print("\n=== Procesando consumos ===")
    
    with open('ejemplo_consumos.xml', 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(
        f'{BASE_URL}/procesarConsumos',
        data=xml_content,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_consultar_datos():
    """Prueba consulta de datos"""
    print("\n=== Consultando datos del sistema ===")
    response = requests.get(f'{BASE_URL}/consultarDatos')
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data['status'] == 'success':
        print(f"Recursos: {len(data['data']['recursos'])}")
        print(f"Categorías: {len(data['data']['categorias'])}")
        print(f"Configuraciones: {len(data['data']['configuraciones'])}")
        print(f"Clientes: {len(data['data']['clientes'])}")
        print(f"Facturas: {len(data['data']['facturas'])}")

def test_crear_recurso():
    """Prueba creación de recurso individual"""
    print("\n=== Creando recurso ===")
    
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
    print(f"Response: {response.json()}")

def test_crear_cliente():
    """Prueba creación de cliente individual"""
    print("\n=== Creando cliente ===")
    
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
    print(f"Response: {response.json()}")

def test_crear_instancia():
    """Prueba creación de instancia"""
    print("\n=== Creando instancia ===")
    
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
    print(f"Response: {response.json()}")

def test_generar_facturas():
    """Prueba generación de facturas"""
    print("\n=== Generando facturas ===")
    
    data = {
        'fechaInicio': '01/01/2025',
        'fechaFin': '31/01/2025'
    }
    
    response = requests.post(f'{BASE_URL}/generarFacturas', json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result['status'] == 'success':
        print(f"Facturas generadas: {len(result['facturas'])}")
        for factura in result['facturas']:
            print(f"\nFactura #{factura['numero']}")
            print(f"Cliente: {factura['nombre_cliente']} - NIT: {factura['nit_cliente']}")
            print(f"Total: ${factura['total']:.2f}")

def test_obtener_factura():
    """Prueba obtención de factura específica"""
    print("\n=== Obteniendo factura #1 ===")
    
    response = requests.get(f'{BASE_URL}/obtenerFactura/1')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        factura = result['factura']
        print(f"\nFactura #{factura['numero']}")
        print(f"Cliente: {factura['nombre_cliente']}")
        print(f"Fecha: {factura['fecha']}")
        print(f"Total: ${factura['total']:.2f}")
        print(f"\nDetalles:")
        for detalle in factura['detalles']:
            print(f"  - {detalle['nombre_instancia']}: ${detalle['subtotal']:.2f}")

def test_analizar_ventas_categorias():
    """Prueba análisis de ventas por categorías"""
    print("\n=== Análisis de ventas por categorías ===")
    
    data = {
        'fechaInicio': '01/01/2025',
        'fechaFin': '31/01/2025'
    }
    
    response = requests.post(f'{BASE_URL}/analizarVentasCategorias', json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nTop configuraciones por ingresos:")
        for i, item in enumerate(result['analisis'][:5], 1):
            print(f"{i}. {item['configuracion']} ({item['categoria']})")
            print(f"   Ingresos: ${item['ingresos']:.2f}")
            print(f"   Instancias facturadas: {item['instancias_facturadas']}")

def test_analizar_ventas_recursos():
    """Prueba análisis de ventas por recursos"""
    print("\n=== Análisis de ventas por recursos ===")
    
    data = {
        'fechaInicio': '01/01/2025',
        'fechaFin': '31/01/2025'
    }
    
    response = requests.post(f'{BASE_URL}/analizarVentasRecursos', json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nTop recursos por ingresos:")
        for i, item in enumerate(result['analisis'][:5], 1):
            print(f"{i}. {item['recurso']} ({item['abreviatura']})")
            print(f"   Ingresos: ${item['ingresos']:.2f}")
            print(f"   Horas totales: {item['horas_totales']:.2f}")

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("PRUEBAS DEL API - Tecnologías Chapinas S.A.")
    print("=" * 60)
    
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
        
        print("\n" + "=" * 60)
        print("PRUEBAS COMPLETADAS")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] No se pudo conectar al servidor.")
        print("Asegúrate de que el API Flask esté ejecutándose en http://localhost:5000")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")

if __name__ == '__main__':
    main()