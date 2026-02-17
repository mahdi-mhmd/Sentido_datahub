from View.MainElements.IconPath import icon

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit


class OrderRemoveDialog(QDialog):
    remove_requested = Signal()
    close_requested = Signal()
    name_changed = Signal(str)

    def __init__(self, theme, name_list):
        super(OrderRemoveDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Remove (Order)")
        self.setMinimumSize(400, 150)
        self.setMaximumSize(550, 250)

        self.order_id = QLineEdit(self)

        self.remove_button = QPushButton("Remove", self)
        self.close_button = QPushButton("Close", self)

        self.name_list = name_list

        layout = QVBoxLayout(self)
        self.setup_widgets(layout)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()
        layout.insertStretch(1, 1)

    def setup_widgets(self, layout):
        h_layout = QHBoxLayout()
        font = self.font()
        font.setPointSize(12)

        v_layout = QVBoxLayout()
        self.order_id.setFont(font)
        v_layout.addWidget(QLabel("Order-ID"))
        v_layout.addWidget(self.order_id)
        h_layout.addLayout(v_layout)
        h_layout.addStretch(1)
        layout.addLayout(h_layout)

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.remove_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.remove_button.clicked.connect(self.remove_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)

    def setup_style(self):
        base_button_style = """
        QPushButton {
            padding: 3px 20px; 
            border-radius: 5px;
        }"""
        base_lineedit_style = """
        QLineEdit {
            border: none;
            border-bottom: 2px solid gray;
        }"""
        if self.is_dark:
            self.setWindowIcon(QIcon(icon("Minus_light.png")))
            theme_button_style = """
            QPushButton {
                background-color: #2f2f2f;
                border: 1px solid #b03b02; 
            }"""
            theme_lineedit_style=""" 
            QLineEdit:focus {
                border-bottom: 2px solid #b03b02;
            }"""
        else:
            self.setWindowIcon(QIcon(icon("Minus_light.png")))
            theme_button_style = """
            QPushButton {
                background-color: white;
                border: 1px solid #ff6f29; 
            }"""
            theme_lineedit_style = """ 
            QLineEdit:focus {
                border-bottom: 2px solid #ff6f29;
            }"""

        self.order_id.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.remove_button.setStyleSheet(base_button_style + theme_button_style)