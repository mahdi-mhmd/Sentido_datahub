from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QSpinBox

from View.MainElements.IconPath import icon


class ECInsertDialog(QDialog):
    insert_requested = Signal()
    close_requested = Signal()
    type_changed = Signal(str)

    def __init__(self, theme, type_list):
        super(ECInsertDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Insert (Component)")
        self.setMinimumSize(700, 250)
        self.setMaximumSize(800, 350)

        self.ec_type = QComboBox(self)
        self.ec_part_number = QComboBox(self)
        self.ec_marking = QComboBox(self)
        self.ec_footprint = QComboBox(self)
        self.ec_manufacturer = QComboBox(self)

        self.ec_price = QSpinBox(self)
        self.ec_qty = QSpinBox(self)
        self.ec_comment = QLineEdit(self)

        self.insert_button = QPushButton("Insert", self)
        self.close_button = QPushButton("Close", self)

        self.type_list = type_list

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

        self.ec_type.addItems(self.type_list)
        self.ec_type.setCurrentIndex(-1)

        for combobox, text in [(self.ec_type, "Type"), (self.ec_part_number, "Part number"),(self.ec_marking, "Marking"),
                               (self.ec_footprint, "Footprint"), (self.ec_manufacturer, "Manufacturer")]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout,1)

        layout.addLayout(h_layout)
        h_layout = QHBoxLayout()

        for spinbox, text, in ((self.ec_qty, "Qty"),
                               (self.ec_price, "Price")):
            spinbox.setFont(font)
            spinbox.setRange(0, 100000)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(spinbox)
            h_layout.addLayout(v_layout, 1)

        self.ec_comment.setFont(font)
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Comment"))
        v_layout.addWidget(self.ec_comment)
        h_layout.addLayout(v_layout, 3)

        layout.addLayout(h_layout)

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.insert_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.insert_button.clicked.connect(self.insert_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.ec_type.currentIndexChanged.connect(lambda _:self.type_changed.emit(self.ec_type.currentText()))

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
            height: 8px;
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
            self.setWindowIcon(QIcon(icon("Plus_light.png")))
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
            self.setWindowIcon(QIcon(icon("Plus_dark.png")))
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

        for combobox in [self.ec_type, self.ec_part_number,self.ec_marking ,self.ec_footprint, self.ec_manufacturer]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        for spinbox in [self.ec_qty, self.ec_price]:
            spinbox.setStyleSheet(base_spinbox_style + theme_spinbox_style)

        self.ec_comment.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.insert_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self, part_numbers,markings ,footprints, manufacturers):
        for combobox, data in ((self.ec_part_number, part_numbers), (self.ec_marking, markings),
                               (self.ec_footprint, footprints),(self.ec_manufacturer, manufacturers)):
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentIndex(-1)
