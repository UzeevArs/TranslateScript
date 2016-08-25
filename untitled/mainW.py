import sys
import tmp
import threading

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType

Path = 'C:\\Users\\Jeggy\\Desktop\\PMSx_V3.23\\'
app = QApplication(sys.argv)
app.setApplicationName('untitled')
form_class, base_class = loadUiType('translateWindow.ui')
con1 = '\".*\"|\'.*'
con2 = '[一-龯ぁ-んァ-ンぁ-ゔゞァ-・ヽヾ゛゜ーバ－コﾘﾄﾗｲﾌ]\w*'
t = threading.Thread(target=tmp.translateFunction, args=(Path, con1, con2))

class MainWindow(QDialog, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setupUi(self)

    def clickButton(self):
        Path = self.pathEdit.text().replace('\\', "\\\\")
        self.rexEdit.setText(Path)

        t.start()
        #tmp.translateFunction(Path,con1,con2)
        return print(Path)


#------------------------------------------------------------#
form = MainWindow()
form.setWindowTitle('untitled')
form.show()
sys.exit(app.exec_())#