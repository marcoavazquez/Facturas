from Facturas import Factura
import sys
import os
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtGui import QFileDialog

#f = Factura(rutaxml)
app = QApplication(sys.argv)

class main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumSize(500,400)
        self.setWindowTitle("Facturas")
        self.btn_carpeta = QPushButton("Seleccionar Carpeta",self)
        self.btn_carpeta.move(5,5)
        self.btn_carpeta.clicked.connect(self.abrirCarpeta)
        self.lbl_ruta = QLabel("",self)
        self.lbl_ruta.move(10,30)
        self.lbl_ruta.setMinimumSize(350,20)
        self.lbl_archivoscopiados = QLabel("",self)
        self.lbl_archivoscopiados.move(8,60)
        self.lbl_archivoscopiados.setMinimumSize(390,300)

    def run(self):
        self.show()
        app.exec_()

    def abrirCarpeta(self):
        QFileDialog(self).setFileMode(QFileDialog.Directory)
        QFileDialog(self).setOption(QFileDialog.ShowDirsOnly)
        self.ruta = QFileDialog(self).getExistingDirectory(self,"Abrir Carpeta")
        self.ruta += '/'
        if self.ruta:
            self.leerArchivos(self.ruta)
            self.copiarArchivos()
            self.lbl_ruta.setText("Ruta: %s" % str(self.ruta))
            print self.ruta
        else:
            self.lbl_ruta.setText("No se ha seleccionado carpeta")

    def leerArchivos(self,ruta):
        self.arc = os.listdir(ruta)

    def copiarArchivos(self):
        rutaServ = "FacturasCopiada/"
        for a in self.arc:
            fullruta = self.ruta + a
            if a[len(a)-3:len(a)] == "xml":
                f = Factura(fullruta)
                print "+++++++++++++++++++++++++++++++++++++++++++++"
                print "RFC del Emisor: ",f.rfcEmisor()
                print "RFC del Cliente: ",f.rfcCliente()
                print "RFC del Nombre del emisor: ",f.nombreEmisor()
                print "Anho de factura: ",f.anhoFactura()
                print "Mes de factura: ",f.mesFactura()
                print "+++++++++++++++++++++++++++++++++++++++++++++"
            else:
                print a + " no es un archivo XML"

    def comprobarPDF(self,nombXml):
        return nombXml

app_main = main()
app_main.run()