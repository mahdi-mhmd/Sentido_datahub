from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QSpinBox

from View.MainElements.IconPath import icon


class ProductEditDialog(QDialog):
    edit_requested = Signal()
    close_requested = Signal()
    type_changed = Signal(str)

    def __init__(self, theme, type_list, current_data):
        super(ProductEditDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Edit (Product)")
        self.setMinimumSize(700, 250)
        self.setMaximumSize(800, 350)

        self.product_type = QComboBox(self)
        self.product_name = QComboBox(self)
        self.product_color = QComboBox(self)
        self.product_qty = QSpinBox(self)
        self.product_price = QSpinBox(self)
        self.product_comment = QLineEdit(self)

        self.edit_button = QPushButton("Edit", self)
        self.close_button = QPushButton("Close", self)

        self.type_list = type_list
        self.current_data = current_data

        layout = QVBoxLayout(self)
        self.setup_widgets(layout)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()
        layout.insertStretch(2, 1)

    def setup_widgets(self, layout):
        h_layout = QHBoxLayout()
        font = self.font()
        font.setPointSize(12)

        self.product_type.addItems(self.type_list)

        for combobox, text, data in [(self.product_type, "Type", self.current_data[0]),(self.product_name, "Name", self.current_data[1]),
                                     (self.product_color, "Color",self.current_data[2])]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setCurrentText(data)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout,1)

        for spinbox,text,data in ((self.product_qty, "Qty",self.current_data[3]), (self.product_price, "Price",self.current_data[4])):
            spinbox.setFont(font)
            spinbox.setRange(0, 100000)
            spinbox.setValue(data)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(spinbox)
            h_layout.addLayout(v_layout, 1)

        layout.addLayout(h_layout)
        h_layout = QHBoxLayout()

        self.product_comment.setFont(font)
        self.product_comment.setText(self.current_data[5])
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Comment"))
        v_layout.addWidget(self.product_comment)
        h_layout.addLayout(v_layout, 4)

        layout.addLayout(h_layout)

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.edit_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.edit_button.clicked.connect(self.edit_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.product_type.currentIndexChanged.connect(lambda _: self.type_changed.emit(self.product_type.currentText()))

    def setup_style(self):
        base_combobox_style = """
        QComboBox {
            padding-right: 0px; 
            border: none;
            border-bottom: 2px solid gray;
        }
        QComboBox QLineEdit {
            border: none;
            background: transparent;
            border-bottom: 2px solid gray;
        }
        QComboBox::down-arrow {
            width: 8px;
            height: 2px;
        }"""
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
        base_spinbox_style = """
        QSpinBox {
            border: none;
            border-bottom: 2px solid gray;
            padding-right: 15px;
        }
        QSpinBox::up-button, 
        QSpinBox::down-button {
            subcontrol-origin: border;
            width: 0px;
            border: none;
        }
        QSpinBox::up-arrow, 
        QSpinBox::down-arrow {
            image: none;
        }"""

        if self.is_dark:
            self.setWindowIcon(QIcon(icon("Edit_light.png")))
            theme_combobox_style = """
            QComboBox:focus {
            border-bottom: 2px solid #b03b02; 
            }
            QComboBox QLineEdit:focus {
            border-bottom: 2px solid #b03b02;
            }"""
            theme_button_style = """
            QPushButton {
                background-color: #2f2f2f;
                border: 1px solid #b03b02; 
            }"""
            theme_lineedit_style=""" 
            QLineEdit:focus {
                border-bottom: 2px solid #b03b02;
            }"""
            theme_spinbox_style = """
            QSpinBox:focus {
                border-bottom: 2px solid #b03b02;
            }"""

        else:
            self.setWindowIcon(QIcon(icon("Edit_dark.png")))
            theme_combobox_style = """
            QComboBox:focus {
            border-bottom: 2px solid #ff6f29; 
            }
            QComboBox QLineEdit:focus {
            border-bottom: 2px solid #ff6f29;
            }"""
            theme_button_style = """
            QPushButton {
                background-color: white;
                border: 1px solid #ff6f29; 
            }"""
            theme_lineedit_style = """ 
            QLineEdit:focus {
                border-bottom: 2px solid #ff6f29;
            }"""
            theme_spinbox_style = """
            QSpinBox:focus {
                border-bottom: 2px solid #ff6f29;
            }"""

        for combobox in [self.product_type, self.product_name,self.product_color]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        for spinbox in [self.product_qty, self.product_price]:
            spinbox.setStyleSheet(base_spinbox_style + theme_spinbox_style)

        self.product_comment.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.edit_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self, names, colors):
        for combobox, data in ((self.product_name, names),(self.product_color, colors)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)