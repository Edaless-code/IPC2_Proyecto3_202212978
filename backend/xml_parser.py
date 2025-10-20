"""
Módulo para procesar archivos XML de configuración y consumo
Incluye validaciones y uso de expresiones regulares
"""
import xml.etree.ElementTree as ET
import re
from datetime import datetime
from typing import Tuple, Optional, Dict, List
from models import (Recurso, Categoria, Configuracion, Cliente, 
                     Instancia, Consumo)


class XMLParser:
    """Clase para parsear archivos XML del sistema"""
    
    @staticmethod
    def validar_nit(nit: str) -> bool:
        """Valida formato de NIT: números-dígito (0-9 o K)"""
        patron = r'^\d+-[0-9K]$'
        return bool(re.match(patron, nit))
    
    @staticmethod
    def extraer_fecha(texto: str) -> Optional[datetime]:
        """Extrae fecha en formato dd/mm/yyyy de un texto"""
        patron = r'(\d{2})/(\d{2})/(\d{4})'
        match = re.search(patron, texto)
        
        if match:
            dia, mes, anio = match.groups()
            try:
                return datetime(int(anio), int(mes), int(dia))
            except ValueError:
                return None
        return None
    
    @staticmethod
    def extraer_fecha_hora(texto: str) -> Optional[datetime]:
        """Extrae fecha y hora en formato dd/mm/yyyy hh:mm de un texto"""
        patron = r'(\d{2})/(\d{2})/(\d{4})\s+(\d{2}):(\d{2})'
        match = re.search(patron, texto)
        
        if match:
            dia, mes, anio, hora, minuto = match.groups()
            try:
                return datetime(int(anio), int(mes), int(dia), 
                              int(hora), int(minuto))
            except ValueError:
                return None
        return None
    
    @staticmethod
    def parsear_configuracion(xml_string: str) -> Tuple[Dict, Dict, Dict, Dict]:
        """
        Parsea el XML de configuración
        Retorna: (recursos, categorias, configuraciones, clientes)
        """
        recursos = {}
        categorias = {}
        configuraciones = {}
        clientes = {}
        
        try:
            root = ET.fromstring(xml_string)
            
            # Procesar recursos
            lista_recursos = root.find('listaRecursos')
            if lista_recursos is not None:
                for recurso_elem in lista_recursos.findall('recurso'):
                    id_recurso = int(recurso_elem.get('id'))
                    nombre = recurso_elem.find('nombre').text.strip()
                    abreviatura = recurso_elem.find('abreviatura').text.strip()
                    metrica = recurso_elem.find('metrica').text.strip()
                    tipo = recurso_elem.find('tipo').text.strip()
                    valor_x_hora = float(recurso_elem.find('valorXhora').text.strip())
                    
                    recurso = Recurso(id_recurso, nombre, abreviatura, 
                                     metrica, tipo, valor_x_hora)
                    recursos[id_recurso] = recurso
            
            # Procesar categorías y configuraciones
            lista_categorias = root.find('listaCategorias')
            if lista_categorias is not None:
                for cat_elem in lista_categorias.findall('categoria'):
                    id_cat = int(cat_elem.get('id'))
                    nombre = cat_elem.find('nombre').text.strip()
                    descripcion = cat_elem.find('descripcion').text.strip()
                    carga_trabajo = cat_elem.find('cargaTrabajo').text.strip()
                    
                    categoria = Categoria(id_cat, nombre, descripcion, carga_trabajo)
                    
                    # Procesar configuraciones de la categoría
                    lista_configs = cat_elem.find('listaConfiguraciones')
                    if lista_configs is not None:
                        for config_elem in lista_configs.findall('configuracion'):
                            id_config = int(config_elem.get('id'))
                            nombre_config = config_elem.find('nombre').text.strip()
                            desc_config = config_elem.find('descripcion').text.strip()
                            
                            configuracion = Configuracion(id_config, nombre_config, 
                                                          desc_config)
                            
                            # Procesar recursos de la configuración
                            recursos_config = config_elem.find('recursosConfiguracion')
                            if recursos_config is not None:
                                for rec_elem in recursos_config.findall('recurso'):
                                    id_rec = int(rec_elem.get('id'))
                                    cantidad = float(rec_elem.text.strip())
                                    configuracion.agregar_recurso(id_rec, cantidad)
                            
                            configuraciones[id_config] = configuracion
                            categoria.agregar_configuracion(configuracion)
                    
                    categorias[id_cat] = categoria
            
            # Procesar clientes e instancias
            lista_clientes = root.find('listaClientes')
            if lista_clientes is not None:
                for cliente_elem in lista_clientes.findall('cliente'):
                    nit = cliente_elem.get('nit')
                    
                    # Validar NIT
                    if not XMLParser.validar_nit(nit):
                        print(f"NIT inválido: {nit}")
                        continue
                    
                    nombre = cliente_elem.find('nombre').text.strip()
                    usuario = cliente_elem.find('usuario').text.strip()
                    clave = cliente_elem.find('clave').text.strip()
                    direccion = cliente_elem.find('direccion').text.strip()
                    correo = cliente_elem.find('correoElectronico').text.strip()
                    
                    cliente = Cliente(nit, nombre, usuario, clave, 
                                     direccion, correo)
                    
                    # Procesar instancias del cliente
                    lista_instancias = cliente_elem.find('listaInstancias')
                    if lista_instancias is not None:
                        for inst_elem in lista_instancias.findall('instancia'):
                            id_inst = int(inst_elem.get('id'))
                            id_config = int(inst_elem.find('idConfiguracion').text.strip())
                            nombre_inst = inst_elem.find('nombre').text.strip()
                            
                            # Extraer fecha de inicio
                            fecha_inicio_text = inst_elem.find('fechaInicio').text
                            fecha_inicio = XMLParser.extraer_fecha(fecha_inicio_text)
                            
                            if not fecha_inicio:
                                print(f"Fecha inválida para instancia {id_inst}")
                                continue
                            
                            estado = inst_elem.find('estado').text.strip()
                            
                            # Extraer fecha final si existe
                            fecha_final = None
                            fecha_final_elem = inst_elem.find('fechaFinal')
                            if fecha_final_elem is not None and fecha_final_elem.text:
                                fecha_final = XMLParser.extraer_fecha(fecha_final_elem.text)
                            
                            instancia = Instancia(id_inst, id_config, nombre_inst,
                                                fecha_inicio, estado, fecha_final)
                            cliente.agregar_instancia(instancia)
                    
                    clientes[nit] = cliente
            
        except ET.ParseError as e:
            print(f"Error al parsear XML: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        return recursos, categorias, configuraciones, clientes
    
    @staticmethod
    def parsear_consumos(xml_string: str) -> List[Tuple[str, int, Consumo]]:
        """
        Parsea el XML de consumos
        Retorna lista de tuplas: (nit_cliente, id_instancia, consumo)
        """
        consumos = []
        
        try:
            root = ET.fromstring(xml_string)
            
            for consumo_elem in root.findall('consumo'):
                nit = consumo_elem.get('nitCliente')
                id_instancia = int(consumo_elem.get('idInstancia'))
                tiempo = float(consumo_elem.find('tiempo').text.strip())
                
                fecha_hora_text = consumo_elem.find('fechaHora').text
                fecha_hora = XMLParser.extraer_fecha_hora(fecha_hora_text)
                
                if not fecha_hora:
                    print(f"Fecha/hora inválida para consumo de instancia {id_instancia}")
                    continue
                
                if not XMLParser.validar_nit(nit):
                    print(f"NIT inválido: {nit}")
                    continue
                
                consumo = Consumo(id_instancia, tiempo, fecha_hora)
                consumos.append((nit, id_instancia, consumo))
                
        except ET.ParseError as e:
            print(f"Error al parsear XML de consumos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        return consumos


class XMLGenerator:
    """Clase para generar archivos XML de salida (base de datos)"""
    
    @staticmethod
    def generar_xml_recursos(recursos: Dict[int, Recurso]) -> str:
        """Genera XML con los recursos almacenados"""
        root = ET.Element('recursos')
        
        for recurso in recursos.values():
            rec_elem = ET.SubElement(root, 'recurso', id=str(recurso.id))
            ET.SubElement(rec_elem, 'nombre').text = recurso.nombre
            ET.SubElement(rec_elem, 'abreviatura').text = recurso.abreviatura
            ET.SubElement(rec_elem, 'metrica').text = recurso.metrica
            ET.SubElement(rec_elem, 'tipo').text = recurso.tipo
            ET.SubElement(rec_elem, 'valorXhora').text = str(recurso.valor_x_hora)
        
        return XMLGenerator._prettify(root)
    
    @staticmethod
    def generar_xml_clientes(clientes: Dict[str, Cliente]) -> str:
        """Genera XML con los clientes almacenados"""
        root = ET.Element('clientes')
        
        for cliente in clientes.values():
            cli_elem = ET.SubElement(root, 'cliente', nit=cliente.nit)
            ET.SubElement(cli_elem, 'nombre').text = cliente.nombre
            ET.SubElement(cli_elem, 'usuario').text = cliente.usuario
            ET.SubElement(cli_elem, 'clave').text = cliente.clave
            ET.SubElement(cli_elem, 'direccion').text = cliente.direccion
            ET.SubElement(cli_elem, 'correoElectronico').text = cliente.correo_electronico
            
            instancias_elem = ET.SubElement(cli_elem, 'instancias')
            for instancia in cliente.instancias.values():
                inst_elem = ET.SubElement(instancias_elem, 'instancia', id=str(instancia.id))
                ET.SubElement(inst_elem, 'idConfiguracion').text = str(instancia.id_configuracion)
                ET.SubElement(inst_elem, 'nombre').text = instancia.nombre
                ET.SubElement(inst_elem, 'fechaInicio').text = instancia.fecha_inicio.strftime('%d/%m/%Y')
                ET.SubElement(inst_elem, 'estado').text = instancia.estado
                if instancia.fecha_final:
                    ET.SubElement(inst_elem, 'fechaFinal').text = instancia.fecha_final.strftime('%d/%m/%Y')
                
                consumos_elem = ET.SubElement(inst_elem, 'consumos')
                for consumo in instancia.consumos:
                    cons_elem = ET.SubElement(consumos_elem, 'consumo')
                    ET.SubElement(cons_elem, 'tiempo').text = str(consumo.tiempo)
                    ET.SubElement(cons_elem, 'fechaHora').text = consumo.fecha_hora.strftime('%d/%m/%Y %H:%M')
                    ET.SubElement(cons_elem, 'facturado').text = str(consumo.facturado)
        
        return XMLGenerator._prettify(root)
    
    @staticmethod
    def _prettify(elem, level=0):
        """Formatea el XML con indentación"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                XMLGenerator._prettify(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
        return ET.tostring(elem, encoding='unicode')