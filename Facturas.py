from xml.dom import minidom

class Factura():
    def __init__(self,rutaxml):
        self.nombre_archivo = ""
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

#f = Factura("/home/marco/Dropbox/facturas/AUVI890706GD2_561_CPA0809035MA.xml")
#print "RFC del Emisor: ",f.rfcEmisor()
#print "RFC del Cliente: ",f.rfcCliente()
#print "RFC del Nombre del emisor: ",f.nombreEmisor()
#print "Anho de factura: ",f.anhoFactura()
#print "Mes de factura: ",f.mesFactura()