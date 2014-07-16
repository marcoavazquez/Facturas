# -*- coding: UTF-8 -*-
from xml.dom import minidom

class Factura():
    def __init__(self,rutaxml):
        self.nodos = minidom.parse(rutaxml).childNodes
        self.emisor = self.nodos[0].getElementsByTagName("cfdi:Emisor")
        self.fecha = self.nodos[0].attributes.get("fecha").value

    def rfcCliente(self):
        cliente = self.nodos[0].getElementsByTagName("cfdi:Receptor")
        self.rfc_cliente = cliente[0].attributes.get("rfc").value
        return self.rfc_cliente

    def rfcEmisor(self):
        self.rfc_emisor = self.emisor[0].attributes.get("rfc").value
        return self.rfc_emisor

    def nombreEmisor(self):
        self.nombre_emisor = self.emisor[0].attributes.get("nombre").value
        return self.nombre_emisor

    def anhoFactura(self):
        self.anho = self.fecha[:4]
        return self.anho

    def mesFactura(self):
        self.mes = self.fecha[5:7]
        return self.mes
