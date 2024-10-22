"""
Vistas de la aplicación cloud_app
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.conf import settings
import requests
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

API_URL = settings.API_BASE_URL


def index(request):
    """Página principal"""
    return render(request, 'index.html')


def enviar_configuracion(request):
    """Enviar archivo XML de configuración"""
    if request.method == 'POST':
        if 'archivo_xml' in request.FILES:
            archivo = request.FILES['archivo_xml']
            try:
                xml_content = archivo.read().decode('utf-8')
                headers = {'Content-Type': 'text/xml; charset=utf-8'}
                response = requests.post(
                    f'{API_URL}/procesarConfiguracion',
                    data=xml_content.encode('utf-8'),
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    stats = result['estadisticas']
                    messages.success(
                        request,
                        f'✅ Configuración procesada exitosamente: '
                        f'{stats["recursos"]} recursos, '
                        f'{stats["categorias"]} categorías, '
                        f'{stats["configuraciones"]} configuraciones, '
                        f'{stats["clientes"]} clientes, '
                        f'{stats["instancias"]} instancias creadas.'
                    )
                else:
                    messages.error(request, 'Error al procesar el archivo XML')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.warning(request, 'Por favor selecciona un archivo XML')
    
    return render(request, 'configuracion.html')


def enviar_consumo(request):
    """Enviar archivo XML de consumos"""
    if request.method == 'POST':
        if 'archivo_xml' in request.FILES:
            archivo = request.FILES['archivo_xml']
            try:
                xml_content = archivo.read().decode('utf-8')
                headers = {'Content-Type': 'text/xml; charset=utf-8'}
                response = requests.post(
                    f'{API_URL}/procesarConsumos',
                    data=xml_content.encode('utf-8'),
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    messages.success(request, f'✅ {result["message"]}')
                else:
                    messages.error(request, 'Error al procesar consumos')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.warning(request, 'Por favor selecciona un archivo XML')
    
    return render(request, 'consumo.html')


def operaciones(request):
    """Menú de operaciones del sistema"""
    return render(request, 'operaciones.html')


def inicializar_sistema(request):
    """Inicializa el sistema (elimina todos los datos)"""
    if request.method == 'POST':
        try:
            response = requests.post(f'{API_URL}/inicializarSistema')
            if response.status_code == 200:
                messages.success(request, '✅ Sistema inicializado correctamente')
            else:
                messages.error(request, 'Error al inicializar el sistema')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('cloud_app:operaciones')


def consultar_datos(request):
    """Consulta todos los datos del sistema"""
    try:
        response = requests.get(f'{API_URL}/consultarDatos')
        if response.status_code == 200:
            data = response.json()['data']
            context = {
                'recursos': data.get('recursos', []),
                'categorias': data.get('categorias', []),
                'configuraciones': data.get('configuraciones', []),
                'clientes': data.get('clientes', []),
                'facturas': data.get('facturas', []),
            }
            return render(request, 'consultar.html', context)
        else:
            messages.error(request, 'Error al consultar datos')
            return redirect('cloud_app:operaciones')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('cloud_app:operaciones')


def crear_datos(request):
    """Página para crear nuevos datos"""
    return render(request, 'crear_datos.html')


def crear_recurso(request):
    """Crea un nuevo recurso"""
    if request.method == 'POST':
        try:
            data = {
                'id': int(request.POST['id']),
                'nombre': request.POST['nombre'],
                'abreviatura': request.POST['abreviatura'],
                'metrica': request.POST['metrica'],
                'tipo': request.POST['tipo'],
                'valorXhora': float(request.POST['valorXhora'])
            }
            
            response = requests.post(f'{API_URL}/crearRecurso', json=data)
            if response.status_code == 201:
                messages.success(request, '✅ Recurso creado exitosamente')
            else:
                result = response.json()
                messages.error(request, f'Error: {result.get("message", "Error desconocido")}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('cloud_app:crear')


def crear_categoria(request):
    """Crea una nueva categoría"""
    if request.method == 'POST':
        try:
            data = {
                'id': int(request.POST['id']),
                'nombre': request.POST['nombre'],
                'descripcion': request.POST['descripcion'],
                'cargaTrabajo': request.POST['cargaTrabajo']
            }
            
            response = requests.post(f'{API_URL}/crearCategoria', json=data)
            if response.status_code == 201:
                messages.success(request, '✅ Categoría creada exitosamente')
            else:
                result = response.json()
                messages.error(request, f'Error: {result.get("message", "Error desconocido")}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('cloud_app:crear')


def crear_configuracion(request):
    """Crea una nueva configuración"""
    if request.method == 'POST':
        try:
            recursos = {}
            recursos_json = request.POST.get('recursos', '{}')
            recursos = json.loads(recursos_json)
            
            data = {
                'id': int(request.POST['id']),
                'nombre': request.POST['nombre'],
                'descripcion': request.POST['descripcion'],
                'idCategoria': int(request.POST['idCategoria']),
                'recursos': recursos
            }
            
            response = requests.post(f'{API_URL}/crearConfiguracion', json=data)
            if response.status_code == 201:
                messages.success(request, '✅ Configuración creada exitosamente')
            else:
                result = response.json()
                messages.error(request, f'Error: {result.get("message", "Error desconocido")}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('cloud_app:crear')


def crear_cliente(request):
    """Crea un nuevo cliente"""
    if request.method == 'POST':
        try:
            data = {
                'nit': request.POST['nit'],
                'nombre': request.POST['nombre'],
                'usuario': request.POST['usuario'],
                'clave': request.POST['clave'],
                'direccion': request.POST['direccion'],
                'correoElectronico': request.POST['correoElectronico']
            }
            
            response = requests.post(f'{API_URL}/crearCliente', json=data)
            if response.status_code == 201:
                messages.success(request, '✅ Cliente creado exitosamente')
            else:
                result = response.json()
                messages.error(request, f'Error: {result.get("message", "Error desconocido")}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('cloud_app:crear')


def crear_instancia(request):
    """Crea una nueva instancia"""
    if request.method == 'POST':
        try:
            data = {
                'nitCliente': request.POST['nitCliente'],
                'id': int(request.POST['id']),
                'idConfiguracion': int(request.POST['idConfiguracion']),
                'nombre': request.POST['nombre'],
                'fechaInicio': request.POST['fechaInicio'],
                'estado': request.POST['estado']
            }
            
            if request.POST.get('fechaFinal'):
                data['fechaFinal'] = request.POST['fechaFinal']
            
            response = requests.post(f'{API_URL}/crearInstancia', json=data)
            if response.status_code == 201:
                messages.success(request, '✅ Instancia creada exitosamente')
            else:
                result = response.json()
                messages.error(request, f'Error: {result.get("message", "Error desconocido")}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('cloud_app:crear')


def cancelar_instancia(request):
    """Cancela una instancia existente"""
    if request.method == 'POST':
        try:
            data = {
                'nitCliente': request.POST['nitCliente'],
                'idInstancia': int(request.POST['idInstancia']),
                'fechaFinal': request.POST['fechaFinal']
            }
            
            response = requests.post(f'{API_URL}/cancelarInstancia', json=data)
            if response.status_code == 200:
                messages.success(request, '✅ Instancia cancelada exitosamente')
            else:
                result = response.json()
                messages.error(request, f'Error: {result.get("message", "Error desconocido")}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('cloud_app:crear')


def facturacion(request):
    """Página de facturación"""
    context = {'facturas': []}
    
    try:
        response = requests.get(f'{API_URL}/consultarDatos')
        if response.status_code == 200:
            data = response.json()['data']
            context['facturas'] = data.get('facturas', [])
    except Exception as e:
        messages.error(request, f'Error al obtener facturas: {str(e)}')
    
    return render(request, 'facturacion.html', context)


def generar_facturas(request):
    """Genera facturas para un rango de fechas"""
    if request.method == 'POST':
        try:
            data = {
                'fechaInicio': request.POST['fechaInicio'],
                'fechaFin': request.POST['fechaFin']
            }
            
            response = requests.post(f'{API_URL}/generarFacturas', json=data)
            if response.status_code == 200:
                result = response.json()
                facturas = result.get('facturas', [])
                messages.success(
                    request,
                    f'✅ {len(facturas)} factura(s) generada(s) exitosamente'
                )
            else:
                result = response.json()
                messages.error(request, f'Error: {result.get("message", "Error desconocido")}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('cloud_app:facturacion')


def reportes(request):
    """Página de reportes"""
    context = {'facturas': []}
    
    try:
        response = requests.get(f'{API_URL}/consultarDatos')
        if response.status_code == 200:
            data = response.json()['data']
            context['facturas'] = data.get('facturas', [])
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'reportes.html', context)


def reporte_factura_pdf(request, numero):
    """Genera PDF con el detalle de una factura"""
    try:
        response = requests.get(f'{API_URL}/obtenerFactura/{numero}')
        if response.status_code != 200:
            messages.error(request, 'Factura no encontrada')
            return redirect('cloud_app:reportes')
        
        factura = response.json()['factura']
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        elements.append(Paragraph('FACTURA', title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        info_data = [
            ['Número de Factura:', f"#{factura['numero']}"],
            ['Cliente:', factura['nombre_cliente']],
            ['NIT:', factura['nit_cliente']],
            ['Fecha:', factura['fecha']],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph('DETALLE DE FACTURACIÓN', styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        for detalle in factura['detalles']:
            inst_data = [
                ['Instancia:', detalle['nombre_instancia']],
                ['Configuración:', detalle['nombre_configuracion']],
                ['Horas Consumidas:', f"{detalle['horas_consumidas']:.2f}h"],
            ]
            
            inst_table = Table(inst_data, colWidths=[2*inch, 4*inch])
            inst_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            elements.append(inst_table)
            elements.append(Spacer(1, 0.1*inch))
            
            recursos_data = [['Recurso', 'Cantidad', 'Métrica', 'Horas', 'Costo/h', 'Total']]
            for rec in detalle['detalles_recursos']:
                recursos_data.append([
                    rec['recurso'],
                    f"{rec['cantidad']:.0f}",
                    rec['metrica'],
                    f"{rec['horas']:.2f}h",
                    f"${rec['costo_hora']:.2f}",
                    f"${rec['costo_total']:.2f}"
                ])
            
            recursos_table = Table(recursos_data, colWidths=[1.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch])
            recursos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#95a5a6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ]))
            elements.append(recursos_table)
            
            subtotal_data = [['Subtotal Instancia:', f"${detalle['subtotal']:.2f}"]]
            subtotal_table = Table(subtotal_data, colWidths=[5*inch, 1*inch])
            subtotal_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
            ]))
            elements.append(Spacer(1, 0.1*inch))
            elements.append(subtotal_table)
            elements.append(Spacer(1, 0.3*inch))
        
        total_data = [['TOTAL A PAGAR:', f"${factura['total']:.2f}"]]
        total_table = Table(total_data, colWidths=[5*inch, 1*inch])
        total_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#27ae60')),
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
        ]))
        elements.append(total_table)
        
        doc.build(elements)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{numero}.pdf"'
        return response
        
    except Exception as e:
        messages.error(request, f'Error al generar PDF: {str(e)}')
        return redirect('cloud_app:reportes')


def reporte_ventas_categorias_pdf(request):
    """Genera PDF con análisis de ventas por categorías"""
    if request.method == 'POST':
        try:
            fecha_inicio = request.POST['fechaInicio']
            fecha_fin = request.POST['fechaFin']
            
            data = {
                'fechaInicio': fecha_inicio,
                'fechaFin': fecha_fin
            }
            response = requests.post(f'{API_URL}/analizarVentasCategorias', json=data)
            
            if response.status_code != 200:
                messages.error(request, 'Error al obtener análisis')
                return redirect('cloud_app:reportes')
            
            analisis = response.json()['analisis']
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            elements.append(Paragraph('ANÁLISIS DE VENTAS POR CATEGORÍAS', title_style))
            elements.append(Spacer(1, 0.2*inch))
            
            periodo_text = f"Período: {fecha_inicio} - {fecha_fin}"
            elements.append(Paragraph(periodo_text, styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            
            if analisis:
                table_data = [['#', 'Configuración', 'Categoría', 'Ingresos', 'Instancias']]
                
                for i, item in enumerate(analisis, 1):
                    table_data.append([
                        str(i),
                        item['configuracion'],
                        item['categoria'],
                        f"${item['ingresos']:.2f}",
                        str(item['instancias_facturadas'])
                    ])
                
                total_ingresos = sum(item['ingresos'] for item in analisis)
                table_data.append([
                    '',
                    '',
                    'TOTAL',
                    f"${total_ingresos:.2f}",
                    ''
                ])
                
                table = Table(table_data, colWidths=[0.5*inch, 2.5*inch, 2*inch, 1.2*inch, 1*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (1, 1), (2, -2), 'LEFT'),
                    ('GRID', (0, 0), (-1, -2), 1, colors.grey),
                    ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ]))
                elements.append(table)
            else:
                elements.append(Paragraph('No hay datos en el período seleccionado', styles['Normal']))
            
            doc.build(elements)
            buffer.seek(0)
            
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="analisis_categorias.pdf"'
            return response
            
        except Exception as e:
            messages.error(request, f'Error al generar PDF: {str(e)}')
            return redirect('cloud_app:reportes')
    
    return redirect('cloud_app:reportes')


def reporte_ventas_recursos_pdf(request):
    """Genera PDF con análisis de ventas por recursos"""
    if request.method == 'POST':
        try:
            fecha_inicio = request.POST['fechaInicio']
            fecha_fin = request.POST['fechaFin']
            
            data = {
                'fechaInicio': fecha_inicio,
                'fechaFin': fecha_fin
            }
            response = requests.post(f'{API_URL}/analizarVentasRecursos', json=data)
            
            if response.status_code != 200:
                messages.error(request, 'Error al obtener análisis')
                return redirect('cloud_app:reportes')
            
            analisis = response.json()['analisis']
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            elements.append(Paragraph('ANÁLISIS DE VENTAS POR RECURSOS', title_style))
            elements.append(Spacer(1, 0.2*inch))
            
            periodo_text = f"Período: {fecha_inicio} - {fecha_fin}"
            elements.append(Paragraph(periodo_text, styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            
            if analisis:
                table_data = [['#', 'Recurso', 'Métrica', 'Horas Totales', 'Ingresos']]
                
                for i, item in enumerate(analisis, 1):
                    table_data.append([
                        str(i),
                        f"{item['recurso']} ({item['abreviatura']})",
                        item['metrica'],
                        f"{item['horas_totales']:.2f}h",
                        f"${item['ingresos']:.2f}"
                    ])
                
                total_ingresos = sum(item['ingresos'] for item in analisis)
                total_horas = sum(item['horas_totales'] for item in analisis)
                table_data.append([
                    '',
                    'TOTAL',
                    '',
                    f"{total_horas:.2f}h",
                    f"${total_ingresos:.2f}"
                ])
                
                table = Table(table_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1.5*inch, 1.2*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (1, 1), (1, -2), 'LEFT'),
                    ('GRID', (0, 0), (-1, -2), 1, colors.grey),
                    ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ]))
                elements.append(table)
            else:
                elements.append(Paragraph('No hay datos en el período seleccionado', styles['Normal']))
            
            doc.build(elements)
            buffer.seek(0)
            
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="analisis_recursos.pdf"'
            return response
            
        except Exception as e:
            messages.error(request, f'Error al generar PDF: {str(e)}')
            return redirect('cloud_app:reportes')
    
    return redirect('cloud_app:reportes')


def ayuda(request):
    """Página de ayuda"""
    context = {
        'estudiante': {
            'nombre': 'Tu Nombre Completo',
            'carnet': '202212978',
            'curso': 'Introducción a la Programación y Computación 2',
            'seccion': 'Tu Sección',
        }
    }
    return render(request, 'ayuda.html', context)