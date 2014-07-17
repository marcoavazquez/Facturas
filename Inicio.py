# -*- coding: UTF-8 -*-

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
        self.rd = "\033[01;31m{0}\033[00m"
        self.grn = "\033[1;36m{0}\033[00m"

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
        else:
            cliente = self.rfcs[f.rfcCliente()]

        rutaServ += "%s//" % cliente
        dir_cliente = os.listdir(rutaServ)
        re_rfc_emisor = "^%s[\W\w]+" % f.rfcEmisor()
        patron = re.compile(re_rfc_emisor)

        #NO PUEDE SER DIR_CLEINTES YA QUE NO EXISTEN LAS CARPETAS , POR LO TANTO EL FOR TERMINA :/
        for dc in dir_cliente:
            if patron.match(dc) == None:
                os.mkdir("%s - %s" % (f.rfcEmisor(),f.nombreEmisor()))
                dir_emisor = "%s - %s" % (f.rfcEmisor(),f.nombreEmisor())
                print "[][-][]",dir_emisor
            else:
                dir_emisor = dc
                print "[][][]",dir_emisor

        if os.path.exists("/ho9me"):
            print "si: ",f.rfcCliente()
        else:
            print "no: ",self.rd.format(rutaServ + cliente + "//" + f.rfcEmisor() + '/.+' + "//" + f.anhoFactura() + "//" + self.meses[f.mesFactura()])
            print f.rfcCliente()
            print apdf


        print "+++++++++++++++++++++++++++++++++++++++++++++"
        print "RFC del Emisor: ",f.rfcEmisor()
        print "RFC del Cliente: ",f.rfcCliente()
        print "RFC del Nombre del emisor: ",f.nombreEmisor()
        print "Anho de factura: ",f.anhoFactura()
        print "Mes de factura: ",f.mesFactura()
        print "+++++++++++++++++++++++++++++++++++++++++++++"
        print apdf

    def comprobarPDF(self):
        self.arc = os.listdir(self.ruta)
        for p in self.arc:
            if not (p[:len(p)-3] + "xml") in self.arc:
                self.mensaje += "<b style='color:red'>Sin XML: %s </b><br>" % p
                self.lbl_archivoscopiados.setText(self.mensaje)
            if p[len(p)-3:len(p)] == "pdf":
                for x in self.arc:
                    if x[len(x)-3:len(x)] == "xml":
                        if p[:len(p)-3] == x[:len(x)-3]:
                            self.copiarArchivos(p,x)
                            print self.rd.format("PDF: %s -> XML: %s" % (p,x))

app_main = main()
app_main.run()