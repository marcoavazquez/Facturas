import sys
from PySide.QtCore import *
from PySide.QtGui import *

app = QApplication(sys.argv)

label = QLabel("Facturas")
label.show()

app.exec_()
sys.exit()