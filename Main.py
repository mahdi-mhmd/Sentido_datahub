import sys
from PySide6.QtWidgets import QApplication

from Controller.MainController import MainController


app = QApplication(sys.argv)
x = MainController()
x.view.show()
app.exec()
