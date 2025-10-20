"""
Modelos POO para el sistema de gestión de nube
Tecnologías Chapinas, S.A.
"""
from datetime import datetime
from typing import List, Dict, Optional

class Recurso:
    """Representa un recurso de infraestructura (Hardware o Software)"""
    
    def __init__(self, id: int, nombre: str, abreviatura: str, metrica: str, 
                 tipo: str, valor_x_hora: float):
        self.id = id
        self.nombre = nombre
        self.abreviatura = abreviatura
        self.metrica = metrica  # GiB, unidades, etc.
        self.tipo = tipo  # Hardware o Software
        self.valor_x_hora = valor_x_hora
    
    def calcular_costo(self, cantidad: float, horas: float) -> float:
        """Calcula el costo de usar este recurso"""
        return cantidad * self.valor_x_hora * horas
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'abreviatura': self.abreviatura,
            'metrica': self.metrica,
            'tipo': self.tipo,
            'valor_x_hora': self.valor_x_hora
        }


class Configuracion:
    """Representa una configuración de recursos"""
    
    def __init__(self, id: int, nombre: str, descripcion: str):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.recursos: Dict[int, float] = {}  # {id_recurso: cantidad}
    
    def agregar_recurso(self, id_recurso: int, cantidad: float):
        """Agrega un recurso a la configuración"""
        self.recursos[id_recurso] = cantidad
    
    def calcular_costo_hora(self, recursos_dict: Dict[int, Recurso]) -> float:
        """Calcula el costo por hora de esta configuración"""
        costo = 0
        for id_recurso, cantidad in self.recursos.items():
            if id_recurso in recursos_dict:
                recurso = recursos_dict[id_recurso]
                costo += recurso.valor_x_hora * cantidad
        return costo
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'recursos': self.recursos
        }


class Categoria:
    """Representa una categoría de configuraciones"""
    
    def __init__(self, id: int, nombre: str, descripcion: str, carga_trabajo: str):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.carga_trabajo = carga_trabajo
        self.configuraciones: Dict[int, Configuracion] = {}
    
    def agregar_configuracion(self, configuracion: Configuracion):
        """Agrega una configuración a la categoría"""
        self.configuraciones[configuracion.id] = configuracion
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'carga_trabajo': self.carga_trabajo,
            'configuraciones': [c.to_dict() for c in self.configuraciones.values()]
        }


class Instancia:
    """Representa una instancia aprovisionada por un cliente"""
    
    def __init__(self, id: int, id_configuracion: int, nombre: str, 
                 fecha_inicio: datetime, estado: str, fecha_final: Optional[datetime] = None):
        self.id = id
        self.id_configuracion = id_configuracion
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.estado = estado  # Vigente o Cancelada
        self.fecha_final = fecha_final
        self.consumos: List['Consumo'] = []
    
    def agregar_consumo(self, consumo: 'Consumo'):
        """Agrega un consumo a la instancia"""
        self.consumos.append(consumo)
    
    def calcular_horas_totales(self, facturadas: bool = False) -> float:
        """Calcula el total de horas consumidas"""
        total = 0
        for consumo in self.consumos:
            if consumo.facturado == facturadas:
                total += consumo.tiempo
        return total
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'id_configuracion': self.id_configuracion,
            'nombre': self.nombre,
            'fecha_inicio': self.fecha_inicio.strftime('%d/%m/%Y'),
            'estado': self.estado,
            'fecha_final': self.fecha_final.strftime('%d/%m/%Y') if self.fecha_final else None,
            'consumos': [c.to_dict() for c in self.consumos]
        }


class Cliente:
    """Representa un cliente del servicio de nube"""
    
    def __init__(self, nit: str, nombre: str, usuario: str, clave: str, 
                 direccion: str, correo_electronico: str):
        self.nit = nit
        self.nombre = nombre
        self.usuario = usuario
        self.clave = clave
        self.direccion = direccion
        self.correo_electronico = correo_electronico
        self.instancias: Dict[int, Instancia] = {}
    
    def agregar_instancia(self, instancia: Instancia):
        """Agrega una instancia al cliente"""
        self.instancias[instancia.id] = instancia
    
    def to_dict(self) -> dict:
        return {
            'nit': self.nit,
            'nombre': self.nombre,
            'usuario': self.usuario,
            'clave': self.clave,
            'direccion': self.direccion,
            'correo_electronico': self.correo_electronico,
            'instancias': [i.to_dict() for i in self.instancias.values()]
        }


class Consumo:
    """Representa el consumo de una instancia"""
    
    def __init__(self, id_instancia: int, tiempo: float, fecha_hora: datetime):
        self.id_instancia = id_instancia
        self.tiempo = tiempo  # En horas
        self.fecha_hora = fecha_hora
        self.facturado = False
    
    def marcar_facturado(self):
        """Marca el consumo como facturado"""
        self.facturado = True
    
    def to_dict(self) -> dict:
        return {
            'id_instancia': self.id_instancia,
            'tiempo': self.tiempo,
            'fecha_hora': self.fecha_hora.strftime('%d/%m/%Y %H:%M'),
            'facturado': self.facturado
        }


class DetalleFactura:
    """Representa el detalle de una factura por instancia"""
    
    def __init__(self, id_instancia: int, nombre_instancia: str, 
                 id_configuracion: int, nombre_configuracion: str):
        self.id_instancia = id_instancia
        self.nombre_instancia = nombre_instancia
        self.id_configuracion = id_configuracion
        self.nombre_configuracion = nombre_configuracion
        self.horas_consumidas = 0
        self.detalles_recursos: List[Dict] = []
        self.subtotal = 0
    
    def agregar_detalle_recurso(self, recurso: Recurso, cantidad: float, 
                                horas: float, costo: float):
        """Agrega el detalle de un recurso"""
        self.detalles_recursos.append({
            'recurso': recurso.nombre,
            'abreviatura': recurso.abreviatura,
            'metrica': recurso.metrica,
            'cantidad': cantidad,
            'horas': horas,
            'costo_hora': recurso.valor_x_hora,
            'costo_total': costo
        })
        self.subtotal += costo
    
    def to_dict(self) -> dict:
        return {
            'id_instancia': self.id_instancia,
            'nombre_instancia': self.nombre_instancia,
            'id_configuracion': self.id_configuracion,
            'nombre_configuracion': self.nombre_configuracion,
            'horas_consumidas': self.horas_consumidas,
            'detalles_recursos': self.detalles_recursos,
            'subtotal': self.subtotal
        }


class Factura:
    """Representa una factura generada para un cliente"""
    
    _contador = 1
    
    def __init__(self, nit_cliente: str, nombre_cliente: str, fecha: datetime):
        self.numero = Factura._contador
        Factura._contador += 1
        self.nit_cliente = nit_cliente
        self.nombre_cliente = nombre_cliente
        self.fecha = fecha
        self.detalles: List[DetalleFactura] = []
        self.total = 0
    
    def agregar_detalle(self, detalle: DetalleFactura):
        """Agrega un detalle de instancia a la factura"""
        self.detalles.append(detalle)
        self.total += detalle.subtotal
    
    def to_dict(self) -> dict:
        return {
            'numero': self.numero,
            'nit_cliente': self.nit_cliente,
            'nombre_cliente': self.nombre_cliente,
            'fecha': self.fecha.strftime('%d/%m/%Y'),
            'detalles': [d.to_dict() for d in self.detalles],
            'total': round(self.total, 2)
        }
    
    @classmethod
    def resetear_contador(cls):
        """Resetea el contador de facturas"""
        cls._contador = 1