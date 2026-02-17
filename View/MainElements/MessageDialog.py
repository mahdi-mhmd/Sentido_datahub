from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout,QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from View.MainElements.IconPath import icon


class MessageDialog(QDialog):

    def __init__(self, theme, message, kind, parent=None):
        super().__init__(parent)
        self.is_dark = theme
        self.setFixedSize(220,100)
        font = self.font()
        font.setPointSize(11)
        self.setFont(font)

        if kind == 1:
            self.setWindowTitle("Success")
            self.setWindowIcon(QIcon(icon("Success.png")))
        else:
            self.setWindowTitle("Error")
            self.setWindowIcon(QIcon(icon("Error.png")))

        label = QLabel(message)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setFixedSize(70,25)

        h_layout = QHBoxLayout()
        h_layout.addWidget(ok_button)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addLayout(h_layout)

        base_button_style = """
        QPushButton {
            padding: 3px 20px; 
            border-radius: 5px;
        }"""
        if self.is_dark:
            theme_button_style = """
            QPushButton {
                background-color: #2f2f2f;
                border: 1px solid #b03b02; 
            }"""
        else:
            theme_button_style = """
            QPushButton {
                background-color: white;
                border: 1px solid #ff6f29; 
            }"""
        ok_button.setStyleSheet(base_button_style + theme_button_style)