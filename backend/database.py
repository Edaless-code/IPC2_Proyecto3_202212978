"""
Gestor de base de datos XML
Maneja la persistencia de datos en archivos XML
"""
import os
from typing import Dict, List, Optional
from datetime import datetime
from models import (Recurso, Categoria, Configuracion, Cliente, 
                     Instancia, Consumo, Factura, DetalleFactura)
from xml_parser import XMLParser, XMLGenerator


class DatabaseManager:
    """Gestor de la base de datos XML"""
    
    def __init__(self, base_path: str = 'data'):
        self.base_path = base_path
        self.recursos: Dict[int, Recurso] = {}
        self.categorias: Dict[int, Categoria] = {}
        self.configuraciones: Dict[int, Configuracion] = {}
        self.clientes: Dict[str, Cliente] = {}
        self.facturas: Dict[int, Factura] = {}
        
        # Crear directorio si no existe
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        
        # Cargar datos existentes
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga datos desde archivos XML"""
        try:
            # Cargar recursos
            recursos_file = os.path.join(self.base_path, 'recursos.xml')
            if os.path.exists(recursos_file):
                with open(recursos_file, 'r', encoding='utf-8') as f:
                    xml_content = f.read()
                    if xml_content.strip():
                        recursos, _, _, _ = XMLParser.parsear_configuracion(
                            f'<?xml version="1.0"?><archivoConfiguraciones><listaRecursos>{xml_content}</listaRecursos></archivoConfiguraciones>'
                        )
                        self.recursos.update(recursos)
            
            # Cargar clientes
            clientes_file = os.path.join(self.base_path, 'clientes.xml')
            if os.path.exists(clientes_file):
                with open(clientes_file, 'r', encoding='utf-8') as f:
                    xml_content = f.read()
                    # Procesar XML de clientes
        except Exception as e:
            print(f"Error al cargar datos: {e}")
    
    def guardar_datos(self):
        """Guarda datos en archivos XML"""
        try:
            # Guardar recursos
            if self.recursos:
                xml_recursos = XMLGenerator.generar_xml_recursos(self.recursos)
                with open(os.path.join(self.base_path, 'recursos.xml'), 
                         'w', encoding='utf-8') as f:
                    f.write(xml_recursos)
            
            # Guardar clientes
            if self.clientes:
                xml_clientes = XMLGenerator.generar_xml_clientes(self.clientes)
                with open(os.path.join(self.base_path, 'clientes.xml'), 
                         'w', encoding='utf-8') as f:
                    f.write(xml_clientes)
            
        except Exception as e:
            print(f"Error al guardar datos: {e}")
    
    def procesar_configuracion(self, xml_string: str) -> Dict[str, int]:
        """
        Procesa un archivo XML de configuración
        Retorna estadísticas de elementos creados
        """
        recursos, categorias, configuraciones, clientes = \
            XMLParser.parsear_configuracion(xml_string)
        
        stats = {
            'recursos': 0,
            'categorias': 0,
            'configuraciones': 0,
            'clientes': 0,
            'instancias': 0
        }
        
        # Agregar recursos nuevos
        for id_rec, recurso in recursos.items():
            if id_rec not in self.recursos:
                self.recursos[id_rec] = recurso
                stats['recursos'] += 1
        
        # Agregar categorías y configuraciones nuevas
        for id_cat, categoria in categorias.items():
            if id_cat not in self.categorias:
                self.categorias[id_cat] = categoria
                stats['categorias'] += 1
        
        for id_conf, configuracion in configuraciones.items():
            if id_conf not in self.configuraciones:
                self.configuraciones[id_conf] = configuracion
                stats['configuraciones'] += 1
        
        # Agregar clientes e instancias nuevos
        for nit, cliente in clientes.items():
            if nit not in self.clientes:
                self.clientes[nit] = cliente
                stats['clientes'] += 1
                stats['instancias'] += len(cliente.instancias)
            else:
                # Cliente existe, agregar instancias nuevas
                for id_inst, instancia in cliente.instancias.items():
                    if id_inst not in self.clientes[nit].instancias:
                        self.clientes[nit].agregar_instancia(instancia)
                        stats['instancias'] += 1
        
        self.guardar_datos()
        return stats
    
    def procesar_consumos(self, xml_string: str) -> int:
        """
        Procesa un archivo XML de consumos
        Retorna cantidad de consumos procesados
        """
        consumos = XMLParser.parsear_consumos(xml_string)
        contador = 0
        
        for nit, id_instancia, consumo in consumos:
            if nit in self.clientes:
                cliente = self.clientes[nit]
                if id_instancia in cliente.instancias:
                    instancia = cliente.instancias[id_instancia]
                    instancia.agregar_consumo(consumo)
                    contador += 1
                else:
                    print(f"Instancia {id_instancia} no encontrada para cliente {nit}")
            else:
                print(f"Cliente {nit} no encontrado")
        
        self.guardar_datos()
        return contador
    
    def crear_recurso(self, id: int, nombre: str, abreviatura: str, 
                     metrica: str, tipo: str, valor_x_hora: float) -> bool:
        """Crea un nuevo recurso"""
        if id in self.recursos:
            return False
        
        recurso = Recurso(id, nombre, abreviatura, metrica, tipo, valor_x_hora)
        self.recursos[id] = recurso
        self.guardar_datos()
        return True
    
    def crear_categoria(self, id: int, nombre: str, descripcion: str, 
                       carga_trabajo: str) -> bool:
        """Crea una nueva categoría"""
        if id in self.categorias:
            return False
        
        categoria = Categoria(id, nombre, descripcion, carga_trabajo)
        self.categorias[id] = categoria
        self.guardar_datos()
        return True
    
    def crear_configuracion(self, id: int, nombre: str, descripcion: str,
                           id_categoria: int, recursos: Dict[int, float]) -> bool:
        """Crea una nueva configuración"""
        if id in self.configuraciones or id_categoria not in self.categorias:
            return False
        
        configuracion = Configuracion(id, nombre, descripcion)
        for id_rec, cantidad in recursos.items():
            if id_rec in self.recursos:
                configuracion.agregar_recurso(id_rec, cantidad)
        
        self.configuraciones[id] = configuracion
        self.categorias[id_categoria].agregar_configuracion(configuracion)
        self.guardar_datos()
        return True
    
    def crear_cliente(self, nit: str, nombre: str, usuario: str, 
                     clave: str, direccion: str, correo: str) -> bool:
        """Crea un nuevo cliente"""
        if nit in self.clientes:
            return False
        
        if not XMLParser.validar_nit(nit):
            return False
        
        cliente = Cliente(nit, nombre, usuario, clave, direccion, correo)
        self.clientes[nit] = cliente
        self.guardar_datos()
        return True
    
    def crear_instancia(self, nit_cliente: str, id: int, id_configuracion: int,
                       nombre: str, fecha_inicio: datetime, estado: str,
                       fecha_final: Optional[datetime] = None) -> bool:
        """Crea una nueva instancia para un cliente"""
        if nit_cliente not in self.clientes:
            return False
        
        if id_configuracion not in self.configuraciones:
            return False
        
        cliente = self.clientes[nit_cliente]
        if id in cliente.instancias:
            return False
        
        instancia = Instancia(id, id_configuracion, nombre, fecha_inicio, 
                             estado, fecha_final)
        cliente.agregar_instancia(instancia)
        self.guardar_datos()
        return True
    
    def cancelar_instancia(self, nit_cliente: str, id_instancia: int, 
                          fecha_final: datetime) -> bool:
        """Cancela una instancia existente"""
        if nit_cliente not in self.clientes:
            return False
        
        cliente = self.clientes[nit_cliente]
        if id_instancia not in cliente.instancias:
            return False
        
        instancia = cliente.instancias[id_instancia]
        instancia.estado = "Cancelada"
        instancia.fecha_final = fecha_final
        self.guardar_datos()
        return True
    
    def generar_facturacion(self, fecha_inicio: datetime, 
                           fecha_fin: datetime) -> List[Factura]:
        """
        Genera facturas para todos los clientes con consumos no facturados
        en el rango de fechas especificado
        """
        facturas_generadas = []
        
        for nit, cliente in self.clientes.items():
            factura = Factura(nit, cliente.nombre, fecha_fin)
            tiene_consumos = False
            
            for instancia in cliente.instancias.values():
                # Filtrar consumos no facturados en el rango de fechas
                consumos_facturar = [
                    c for c in instancia.consumos
                    if not c.facturado and 
                    fecha_inicio <= c.fecha_hora <= fecha_fin
                ]
                
                if consumos_facturar:
                    tiene_consumos = True
                    
                    # Crear detalle de factura para esta instancia
                    configuracion = self.configuraciones.get(instancia.id_configuracion)
                    if not configuracion:
                        continue
                    
                    detalle = DetalleFactura(
                        instancia.id,
                        instancia.nombre,
                        configuracion.id,
                        configuracion.nombre
                    )
                    
                    # Calcular horas totales
                    horas_totales = sum(c.tiempo for c in consumos_facturar)
                    detalle.horas_consumidas = horas_totales
                    
                    # Calcular costo por recurso
                    for id_recurso, cantidad in configuracion.recursos.items():
                        if id_recurso in self.recursos:
                            recurso = self.recursos[id_recurso]
                            costo = recurso.calcular_costo(cantidad, horas_totales)
                            detalle.agregar_detalle_recurso(
                                recurso, cantidad, horas_totales, costo
                            )
                    
                    factura.agregar_detalle(detalle)
                    
                    # Marcar consumos como facturados
                    for consumo in consumos_facturar:
                        consumo.marcar_facturado()
            
            if tiene_consumos:
                self.facturas[factura.numero] = factura
                facturas_generadas.append(factura)
        
        self.guardar_datos()
        return facturas_generadas
    
    def obtener_factura(self, numero: int) -> Optional[Factura]:
        """Obtiene una factura por su número"""
        return self.facturas.get(numero)
    
    def obtener_facturas_por_rango(self, fecha_inicio: datetime, 
                                   fecha_fin: datetime) -> List[Factura]:
        """Obtiene todas las facturas en un rango de fechas"""
        return [
            f for f in self.facturas.values()
            if fecha_inicio <= f.fecha <= fecha_fin
        ]
    
    def analizar_ventas_por_categoria(self, fecha_inicio: datetime,
                                     fecha_fin: datetime) -> List[Dict]:
        """Analiza ingresos por categoría y configuración"""
        analisis = {}
        
        facturas = self.obtener_facturas_por_rango(fecha_inicio, fecha_fin)
        
        for factura in facturas:
            for detalle in factura.detalles:
                id_config = detalle.id_configuracion
                
                if id_config not in analisis:
                    config = self.configuraciones.get(id_config)
                    if config:
                        # Buscar categoría
                        categoria_nombre = "Sin categoría"
                        for cat in self.categorias.values():
                            if id_config in cat.configuraciones:
                                categoria_nombre = cat.nombre
                                break
                        
                        analisis[id_config] = {
                            'configuracion': config.nombre,
                            'categoria': categoria_nombre,
                            'ingresos': 0,
                            'instancias_facturadas': 0
                        }
                
                analisis[id_config]['ingresos'] += detalle.subtotal
                analisis[id_config]['instancias_facturadas'] += 1
        
        # Convertir a lista y ordenar por ingresos
        resultado = list(analisis.values())
        resultado.sort(key=lambda x: x['ingresos'], reverse=True)
        return resultado
    
    def analizar_ventas_por_recurso(self, fecha_inicio: datetime,
                                   fecha_fin: datetime) -> List[Dict]:
        """Analiza ingresos por recurso"""
        analisis = {}
        
        facturas = self.obtener_facturas_por_rango(fecha_inicio, fecha_fin)
        
        for factura in facturas:
            for detalle in factura.detalles:
                for det_recurso in detalle.detalles_recursos:
                    nombre_recurso = det_recurso['recurso']
                    
                    if nombre_recurso not in analisis:
                        analisis[nombre_recurso] = {
                            'recurso': nombre_recurso,
                            'abreviatura': det_recurso['abreviatura'],
                            'metrica': det_recurso['metrica'],
                            'ingresos': 0,
                            'horas_totales': 0
                        }
                    
                    analisis[nombre_recurso]['ingresos'] += det_recurso['costo_total']
                    analisis[nombre_recurso]['horas_totales'] += det_recurso['horas']
        
        # Convertir a lista y ordenar por ingresos
        resultado = list(analisis.values())
        resultado.sort(key=lambda x: x['ingresos'], reverse=True)
        return resultado
    
    def inicializar_sistema(self):
        """Elimina todos los datos del sistema"""
        self.recursos.clear()
        self.categorias.clear()
        self.configuraciones.clear()
        self.clientes.clear()
        self.facturas.clear()
        Factura.resetear_contador()
        
        # Eliminar archivos
        try:
            for archivo in os.listdir(self.base_path):
                ruta = os.path.join(self.base_path, archivo)
                if os.path.isfile(ruta):
                    os.remove(ruta)
        except Exception as e:
            print(f"Error al eliminar archivos: {e}")
    
    def obtener_datos_completos(self) -> Dict:
        """Retorna todos los datos del sistema"""
        return {
            'recursos': [r.to_dict() for r in self.recursos.values()],
            'categorias': [c.to_dict() for c in self.categorias.values()],
            'configuraciones': [c.to_dict() for c in self.configuraciones.values()],
            'clientes': [c.to_dict() for c in self.clientes.values()],
            'facturas': [f.to_dict() for f in self.facturas.values()]
        }