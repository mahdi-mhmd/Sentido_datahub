from PySide6.QtCore import Signal , QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from View.MainElements.IconPath import icon


class SerialInsertDialog(QDialog):
    insert_requested = Signal()
    close_requested = Signal()
    type_changed = Signal(str)

    def __init__(self, theme, type_list):
        super(SerialInsertDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Insert (Serial)")
        self.setMinimumSize(550, 250)
        self.setMaximumSize(650, 350)

        self.product_type = QComboBox(self)
        self.product_name = QComboBox(self)
        self.product_color = QComboBox(self)

        self.serial_serial = QLineEdit(self)
        self.serial_mac = QLineEdit(self)
        self.serial_comment = QLineEdit(self)

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

        self.product_type.addItems(self.type_list)
        self.product_type.setCurrentIndex(-1)

        if self.is_dark:
            product_png = icon("Product_light.png")
            serial_png = icon("Serial_light.png")
        else:
            product_png = icon("Product_dark.png")
            serial_png = icon("Serial_dark.png")

        product_icon = QPushButton()
        product_icon.setIcon(QIcon(product_png))
        h_layout.addWidget(product_icon)

        for combobox, text in [(self.product_type, "Type"),(self.product_name, "Name"),(self.product_color, "Color")]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout,1)

        layout.addLayout(h_layout)
        h_layout = QHBoxLayout()

        for lineedit,text,num in [(self.serial_serial, "Serial",1),(self.serial_mac, "Mac",1),(self.serial_comment, "Comment",0)]:
            lineedit.setFont(font)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(lineedit)
            if num:
                h_layout.addLayout(v_layout)

        main_v_layout = QVBoxLayout()
        main_v_layout.addLayout(h_layout)
        main_v_layout.addLayout(v_layout)
        h_layout = QHBoxLayout()
        serial_icon = QPushButton()
        serial_icon.setIcon(QIcon(serial_png))
        h_layout.addWidget(serial_icon)
        h_layout.addLayout(main_v_layout)
        layout.addLayout(h_layout)

        for icons in [product_icon, serial_icon]:
            icons.setIconSize(QSize(36, 36))
            icons.setFixedSize(50, 50)
            icons.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }""")

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.insert_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.insert_button.clicked.connect(self.insert_requested.emit)
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
            height: 8px;
        }"""
        base_lineedit_style = """
        QLineEdit {
            border: none;
            border-bottom: 2px solid gray;
        }"""
        base_button_style = """
        QPushButton {
            padding: 3px 20px; 
            border-radius: 5px;
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
            theme_lineedit_style=""" 
            QLineEdit:focus {
                border-bottom: 2px solid #b03b02;
            }"""
            theme_button_style = """
            QPushButton {
                background-color: #2f2f2f;
                border: 1px solid #b03b02; 
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
            theme_lineedit_style = """ 
            QLineEdit:focus {
                border-bottom: 2px solid #ff6f29;
            }"""
            theme_button_style = """
            QPushButton {
                background-color: white;
                border: 1px solid #ff6f29; 
            }"""

        for combobox in [self.product_type, self.product_name,self.product_color]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        for lineedit in [self.serial_serial, self.serial_mac, self.serial_comment]:
            lineedit.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.insert_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self, names, colors):
        for combobox, data in ((self.product_name, names),(self.product_color, colors)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)