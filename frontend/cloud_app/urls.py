"""
URLs de la aplicación cloud_app
"""
from django.urls import path
from . import views

app_name = 'cloud_app'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    
    # Enviar mensajes XML
    path('configuracion/', views.enviar_configuracion, name='configuracion'),
    path('consumo/', views.enviar_consumo, name='consumo'),
    
    # Operaciones del sistema
    path('operaciones/', views.operaciones, name='operaciones'),
    path('inicializar/', views.inicializar_sistema, name='inicializar'),
    path('consultar/', views.consultar_datos, name='consultar'),
    path('crear/', views.crear_datos, name='crear'),
    
    # Crear elementos individuales
    path('crear/recurso/', views.crear_recurso, name='crear_recurso'),
    path('crear/categoria/', views.crear_categoria, name='crear_categoria'),
    path('crear/configuracion/', views.crear_configuracion, name='crear_configuracion'),
    path('crear/cliente/', views.crear_cliente, name='crear_cliente'),
    path('crear/instancia/', views.crear_instancia, name='crear_instancia'),
    path('cancelar/instancia/', views.cancelar_instancia, name='cancelar_instancia'),
    
    # Facturación
    path('facturacion/', views.facturacion, name='facturacion'),
    path('generar-facturas/', views.generar_facturas, name='generar_facturas'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
    path('reporte/factura/<int:numero>/', views.reporte_factura_pdf, name='reporte_factura'),
    path('reporte/ventas-categorias/', views.reporte_ventas_categorias_pdf, name='reporte_ventas_categorias'),
    path('reporte/ventas-recursos/', views.reporte_ventas_recursos_pdf, name='reporte_ventas_recursos'),
    
    # Ayuda
    path('ayuda/', views.ayuda, name='ayuda'),
]