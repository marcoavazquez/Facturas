# -*- coding: UTF-8 -*-
import shutil
from Facturas import Factura
import sys
import re
import os
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtGui import QFileDialog

app = QApplication(sys.argv)

class main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.mensaje =""
        self.setMinimumSize(500,400)
        self.setWindowTitle("Facturas")
        self.btn_carpeta = QPushButton("  Seleccionar Carpeta  ",self)
        self.btn_carpeta.move(10,10)
        self.btn_carpeta.clicked.connect(self.abrirCarpeta)
        self.lbl_ruta = QLabel("",self)
        self.lbl_ruta.move(150,10)
        self.lbl_ruta.setMinimumSize(350,20)
        self.lbl_archivoscopiados = QLabel(self.mensaje,self)
        self.lbl_archivoscopiados.move(10,60)
        self.lbl_archivoscopiados.setMinimumSize(490,300)

        self.rfcs={'CCE110310LXA':'Conev','CPA0809035MA':'CPA','CCS1103109J3':'Cseg','JIBD581227PX8':' David Jimenez Baez',
                'FFG091112LK1':'FMG','GGO121122KQ7':'Geoperfora','VARH7808073I3':'Hector Hugo Vasquez Reyes:',
                'IIC110711R50':'IC','GCK130220QX1':'Kuanasi','MPY110411Q22':'MTZ','PCP121025AI7':'Palenque',
                'HECP760920GE2':'Porfirio Hernandez Cruz','QCO1302203J9':'Quanax','GCT121024N51':'Tepechiapan'}

        self.meses = {'01':'01 - Enero','02':'02 - Febrero','03':'03 - Marzo','04':'04 - Abril','05':'05 - Mayo',
                '06':'06 - Junio','07':'07 - Julio','08':'08 - Agosto','09':'09 - Septiembre','10':'10 - Octubre',
                '11':'11 - Noviembre','12':'12 - Diciembre'}

    def run(self):
        self.show()
        app.exec_()

    def abrirCarpeta(self):
        QFileDialog(self).setFileMode(QFileDialog.Directory)
        QFileDialog(self).setOption(QFileDialog.ShowDirsOnly)
        self.ruta = QFileDialog(self).getExistingDirectory(self,"Abrir Carpeta")
        self.ruta += '//'
        if self.ruta:
            self.lbl_ruta.setText("<b>%s</b>" % str(self.ruta))
            self.comprobarPDF()
        else:
            self.lbl_ruta.setText("No se ha seleccionado carpeta")

    def copiarArchivos(self,apdf,axml):
        rutaServ = "FacturasCopiada//"
        fullrutaxml = self.ruta + axml
        f = Factura(fullrutaxml)

        if not f.rfcCliente() in self.rfcs:
            cliente = "Otros"
            print "Factura no pertenece a las empresas"
        else:
            cliente = self.rfcs[f.rfcCliente()]

        rutaServ += "%s/" % cliente #Ruta + Empresa
        dir_cliente = os.listdir(rutaServ) #lista de proveedores de la empresa
        existe_carp = False

        for i in dir_cliente:
            if f.rfcEmisor() in i: #Busca el RFC dentro de los nombres de Carpetas
                existe_carp = True #existe carpeta
                carp_cliente = i
                break

        if existe_carp:
            rutaServ += "/%s/%s/" % (carp_cliente,f.anhoFactura()) #Ruta hasta al AHNO
            print "Esta carpeta existe: ",carp_cliente
            if os.path.exists(rutaServ): #Si existe carpeta de ANHO
                if os.path.exists(rutaServ + "/" + self.meses[f.mesFactura()]):
                    shutil.copy(self.ruta + axml,rutaServ + "/" + self.meses[f.mesFactura()] + "/" + axml)
                    print "<br>Archivo XML copiado: ",axml
                    self.mensaje += "<br>Archivo %s copiado" % axml
                    shutil.copy(self.ruta + apdf,rutaServ + "/" + self.meses[f.mesFactura()] + "/" + apdf)
                    print "Archivo PDF copiado: ",apdf
                    self.mensaje += "<br>Archivo %s copiado" % apdf
                else:
                    os.mkdir(rutaServ + "/" + self.meses[f.mesFactura()])
                    print "Se crea carpeta mes: ",f.mesFactura()
                    self.mensaje += "<br>Se crea carpeta mes: ",f.mesFactura()
                    shutil.copy(self.ruta + axml,rutaServ + "/" + self.meses[f.mesFactura()] + "/" + axml)
                    print "Archivo XML copiado: ",axml
                    self.mensaje += "<br>Archivo %s copiado" % axml
                    shutil.copy(self.ruta + apdf,rutaServ + "/" + self.meses[f.mesFactura()] + "/" + apdf)
                    print "Archivo PDF copiado: ",apdf
                    self.mensaje += "<br>Archivo %s copiado" % apdf
            else:
                os.mkdir(rutaServ)
                print "Se crea carpeta anho: ",f.anhoFactura()
                os.mkdir(rutaServ + "/" + self.meses[f.mesFactura()])
                print "Se crea carpeta mes: ",f.mesFactura()
                shutil.copy(self.ruta + axml,rutaServ + "/" + self.meses[f.mesFactura()] + "/" + axml)
                print "Archivo XML copiado: ",axml
                self.mensaje += "<br>Archivo %s copiado" % axml
                shutil.copy(self.ruta + apdf,rutaServ + "/" + self.meses[f.mesFactura()] + "/" + apdf)
                print "Archivo PDF copiado: ",apdf
                self.mensaje += "<br>Archivo %s copiado" % apdf
        else:
            os.mkdir(rutaServ + f.rfcEmisor() + " - " + f.nombreEmisor())
            os.mkdir(rutaServ + f.rfcEmisor() + " - " + f.nombreEmisor() + "/" + f.anhoFactura())
            os.mkdir(rutaServ + f.rfcEmisor() + " - " + f.nombreEmisor() + "/" + f.anhoFactura() + "/" + self.meses[f.mesFactura()])
            print "se crea ruta completa"
            self.mensaje += "<br>Creando carpetas..."
            shutil.copy(self.ruta + axml,
                rutaServ + f.rfcEmisor() + " - " + f.nombreEmisor() + "/" + f.anhoFactura() + "/" + self.meses[f.mesFactura()] + "/" + axml)
            print "Archivo XML copiado: ",axml
            self.mensaje += "<br>Archivo %s copiado" % axml
            shutil.copy(self.ruta + apdf,
                rutaServ + f.rfcEmisor() + " - " + f.nombreEmisor() + "/" + f.anhoFactura() + "/" + self.meses[f.mesFactura()] + "/" + apdf)
            print "Archivo PDF copiado: ",apdf
            self.mensaje += "<br>Archivo %s copiado" % apdf

        self.lbl_archivoscopiados.setText(self.mensaje)

    def comprobarPDF(self):
        self.arc = os.listdir(self.ruta)
        for p in self.arc:
            if not (p[:len(p)-3] + "xml") in self.arc:
                self.mensaje += "<b style='color:red'><br>Archivos no copiados: %s </b>" % p
                self.lbl_archivoscopiados.setText(self.mensaje)
            if p[len(p)-3:len(p)] == "pdf":
                for x in self.arc:
                    if x[len(x)-3:len(x)] == "xml":
                        if p[:len(p)-3] == x[:len(x)-3]:
                            self.copiarArchivos(p,x)
                            print ("PDF: %s -> XML: %s \n - + - + - + - + -" % (p,x))

app_main = main()
app_main.run()