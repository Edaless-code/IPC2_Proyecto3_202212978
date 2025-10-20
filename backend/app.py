"""
API REST con Flask para el sistema de gestión de nube
Tecnologías Chapinas, S.A.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from database import DatabaseManager
from xml_parser import XMLParser

app = Flask(__name__)
CORS(app)

# Instancia del gestor de base de datos
db = DatabaseManager()


@app.route('/consultarDatos', methods=['GET'])
def consultar_datos():
    """GET - Consulta todos los datos del sistema"""
    try:
        datos = db.obtener_datos_completos()
        return jsonify({
            'status': 'success',
            'data': datos
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/crearRecurso', methods=['POST'])
def crear_recurso():
    """POST - Crea un nuevo recurso"""
    try:
        data = request.json
        exito = db.crear_recurso(
            data['id'],
            data['nombre'],
            data['abreviatura'],
            data['metrica'],
            data['tipo'],
            float(data['valorXhora'])
        )
        
        if exito:
            return jsonify({
                'status': 'success',
                'message': 'Recurso creado exitosamente'
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'El recurso ya existe'
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/crearCategoria', methods=['POST'])
def crear_categoria():
    """POST - Crea una nueva categoría"""
    try:
        data = request.json
        exito = db.crear_categoria(
            data['id'],
            data['nombre'],
            data['descripcion'],
            data['cargaTrabajo']
        )
        
        if exito:
            return jsonify({
                'status': 'success',
                'message': 'Categoría creada exitosamente'
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'La categoría ya existe'
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/crearConfiguracion', methods=['POST'])
def crear_configuracion():
    """POST - Crea una nueva configuración"""
    try:
        data = request.json
        exito = db.crear_configuracion(
            data['id'],
            data['nombre'],
            data['descripcion'],
            data['idCategoria'],
            data['recursos']  # Dict {idRecurso: cantidad}
        )
        
        if exito:
            return jsonify({
                'status': 'success',
                'message': 'Configuración creada exitosamente'
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Error al crear configuración'
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/crearCliente', methods=['POST'])
def crear_cliente():
    """POST - Crea un nuevo cliente"""
    try:
        data = request.json
        exito = db.crear_cliente(
            data['nit'],
            data['nombre'],
            data['usuario'],
            data['clave'],
            data['direccion'],
            data['correoElectronico']
        )
        
        if exito:
            return jsonify({
                'status': 'success',
                'message': 'Cliente creado exitosamente'
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'El cliente ya existe o NIT inválido'
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/crearInstancia', methods=['POST'])
def crear_instancia():
    """POST - Crea una nueva instancia"""
    try:
        data = request.json
        
        # Parsear fecha
        fecha_inicio = XMLParser.extraer_fecha(data['fechaInicio'])
        if not fecha_inicio:
            return jsonify({
                'status': 'error',
                'message': 'Formato de fecha inválido'
            }), 400
        
        fecha_final = None
        if 'fechaFinal' in data and data['fechaFinal']:
            fecha_final = XMLParser.extraer_fecha(data['fechaFinal'])
        
        exito = db.crear_instancia(
            data['nitCliente'],
            data['id'],
            data['idConfiguracion'],
            data['nombre'],
            fecha_inicio,
            data['estado'],
            fecha_final
        )
        
        if exito:
            return jsonify({
                'status': 'success',
                'message': 'Instancia creada exitosamente'
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Error al crear instancia'
            }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/cancelarInstancia', methods=['POST'])
def cancelar_instancia():
    """POST - Cancela una instancia existente"""
    try:
        data = request.json
        
        fecha_final = XMLParser.extraer_fecha(data['fechaFinal'])
        if not fecha_final:
            return jsonify({
                'status': 'error',
                'message': 'Formato de fecha inválido'
            }), 400
        
        exito = db.cancelar_instancia(
            data['nitCliente'],
            data['idInstancia'],
            fecha_final
        )
        
        if exito:
            return jsonify({
                'status': 'success',
                'message': 'Instancia cancelada exitosamente'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Instancia no encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/procesarConfiguracion', methods=['POST'])
def procesar_configuracion():
    """POST - Procesa archivo XML de configuración"""
    try:
        # Obtener XML del body
        xml_content = request.data.decode('utf-8')
        
        if not xml_content:
            return jsonify({
                'status': 'error',
                'message': 'No se recibió contenido XML'
            }), 400
        
        stats = db.procesar_configuracion(xml_content)
        
        return jsonify({
            'status': 'success',
            'message': 'Configuración procesada exitosamente',
            'estadisticas': stats
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/procesarConsumos', methods=['POST'])
def procesar_consumos():
    """POST - Procesa archivo XML de consumos"""
    try:
        # Obtener XML del body
        xml_content = request.data.decode('utf-8')
        
        if not xml_content:
            return jsonify({
                'status': 'error',
                'message': 'No se recibió contenido XML'
            }), 400
        
        cantidad = db.procesar_consumos(xml_content)
        
        return jsonify({
            'status': 'success',
            'message': f'{cantidad} consumos procesados exitosamente',
            'cantidad': cantidad
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/generarFacturas', methods=['POST'])
def generar_facturas():
    """POST - Genera facturas para un rango de fechas"""
    try:
        data = request.json
        
        fecha_inicio = XMLParser.extraer_fecha(data['fechaInicio'])
        fecha_fin = XMLParser.extraer_fecha(data['fechaFin'])
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({
                'status': 'error',
                'message': 'Formato de fechas inválido'
            }), 400
        
        facturas = db.generar_facturacion(fecha_inicio, fecha_fin)
        
        return jsonify({
            'status': 'success',
            'message': f'{len(facturas)} facturas generadas',
            'facturas': [f.to_dict() for f in facturas]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/obtenerFactura/<int:numero>', methods=['GET'])
def obtener_factura(numero):
    """GET - Obtiene una factura específica"""
    try:
        factura = db.obtener_factura(numero)
        
        if factura:
            return jsonify({
                'status': 'success',
                'factura': factura.to_dict()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Factura no encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/analizarVentasCategorias', methods=['POST'])
def analizar_ventas_categorias():
    """POST - Analiza ventas por categorías y configuraciones"""
    try:
        data = request.json
        
        fecha_inicio = XMLParser.extraer_fecha(data['fechaInicio'])
        fecha_fin = XMLParser.extraer_fecha(data['fechaFin'])
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({
                'status': 'error',
                'message': 'Formato de fechas inválido'
            }), 400
        
        analisis = db.analizar_ventas_por_categoria(fecha_inicio, fecha_fin)
        
        return jsonify({
            'status': 'success',
            'analisis': analisis
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/analizarVentasRecursos', methods=['POST'])
def analizar_ventas_recursos():
    """POST - Analiza ventas por recursos"""
    try:
        data = request.json
        
        fecha_inicio = XMLParser.extraer_fecha(data['fechaInicio'])
        fecha_fin = XMLParser.extraer_fecha(data['fechaFin'])
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({
                'status': 'error',
                'message': 'Formato de fechas inválido'
            }), 400
        
        analisis = db.analizar_ventas_por_recurso(fecha_inicio, fecha_fin)
        
        return jsonify({
            'status': 'success',
            'analisis': analisis
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/inicializarSistema', methods=['POST'])
def inicializar_sistema():
    """POST - Inicializa el sistema (elimina todos los datos)"""
    try:
        db.inicializar_sistema()
        
        return jsonify({
            'status': 'success',
            'message': 'Sistema inicializado correctamente'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    """Ruta raíz - información del API"""
    return jsonify({
        'api': 'Tecnologías Chapinas S.A.',
        'version': '1.0',
        'endpoints': {
            'GET /consultarDatos': 'Consultar todos los datos',
            'POST /crearRecurso': 'Crear nuevo recurso',
            'POST /crearCategoria': 'Crear nueva categoría',
            'POST /crearConfiguracion': 'Crear nueva configuración',
            'POST /crearCliente': 'Crear nuevo cliente',
            'POST /crearInstancia': 'Crear nueva instancia',
            'POST /cancelarInstancia': 'Cancelar instancia',
            'POST /procesarConfiguracion': 'Procesar XML de configuración',
            'POST /procesarConsumos': 'Procesar XML de consumos',
            'POST /generarFacturas': 'Generar facturas',
            'GET /obtenerFactura/<numero>': 'Obtener factura específica',
            'POST /analizarVentasCategorias': 'Análisis por categorías',
            'POST /analizarVentasRecursos': 'Análisis por recursos',
            'POST /inicializarSistema': 'Reiniciar sistema'
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)