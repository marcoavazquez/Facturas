from xml.dom import minidom

class Factura():
    def __init__(self,rutaxml):
        self.nodos = minidom.parse(rutaxml).childNodes

    def RfcEmisor(self):
        emisor = self.nodos[0].getElementsByTagName("cfdi:Emisor")
        self.rfc_emisor = emisor[0].attributes.get("rfc").value
        return self.rfc_emisor

f = Factura("C:\Users\marco\Desktop\\facturas\AUVI890706GD2_561_CPA0809035MA.xml")
print f.RfcEmisor()