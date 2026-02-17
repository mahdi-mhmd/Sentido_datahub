from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from View.MainElements.TableView import TableView

from View.MainElements.IconPath import icon


class OrderDtlSearchDialog(QDialog):
    adv_search_requested = Signal()
    close_requested = Signal()
    type_changed = Signal(str)

    def __init__(self, theme, type_list, headers, info):
        super(OrderDtlSearchDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Search (OrderDtl)")
        self.setMinimumSize(700, 300)

        self.product_type = QComboBox(self)
        self.product_name = QComboBox(self)
        self.product_color = QComboBox(self)
        self.serial_serial = QLineEdit(self)

        self.search_button = QPushButton("Search", self)
        self.close_button = QPushButton("Close", self)

        self.tableview = TableView(self.is_dark, headers, info)

        self.type_list = type_list

        layout = QVBoxLayout(self)
        self.setup_widgets(layout)
        layout.addWidget(self.tableview)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()
        layout.insertStretch(3, 1)

    def setup_widgets(self, layout):
        h_layout = QHBoxLayout()
        font = self.font()
        font.setPointSize(12)

        if self.is_dark:
            product_png = icon("Product_light.png")
            serial_png = icon("Serial_light.png")
        else:
            product_png = icon("Product_dark.png")
            serial_png = icon("Serial_dark.png")

        self.product_type.addItems(self.type_list)
        self.product_type.setCurrentIndex(-1)

        product_icon = QPushButton()
        product_icon.setIcon(QIcon(product_png))
        h_layout.addWidget(product_icon)

        for combobox, text in [(self.product_type, "Type"), (self.product_name, "Name"), (self.product_color, "Color")]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setFixedSize(QSize(130, 27))
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout, 1)

        h_layout.addStretch(1)
        layout.addLayout(h_layout)
        h_layout = QHBoxLayout()

        serial_icon = QPushButton()
        serial_icon.setIcon(QIcon(serial_png))
        h_layout.addWidget(serial_icon)

        v_layout = QVBoxLayout()
        self.serial_serial.setFont(font)
        v_layout.addWidget(QLabel("Serial"))
        v_layout.addWidget(self.serial_serial)
        self.serial_serial.setFixedSize(QSize(130, 27))
        h_layout.addLayout(v_layout)
        h_layout.addStretch()

        layout.addLayout(h_layout)

        for icons in [product_icon, serial_icon]:
            icons.setIconSize(QSize(40, 40))
            icons.setFixedSize(50, 50)
            icons.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }""")


    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.search_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.search_button.clicked.connect(self.adv_search_requested.emit)
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
            self.setWindowIcon(QIcon(icon("ADVSearch_light.png")))
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

        else:
            self.setWindowIcon(QIcon(icon("ADVSearch_dark.png")))
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

        for combobox in [self.product_type, self.product_name, self.product_color]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        self.serial_serial.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.search_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self, names, colors):
        for combobox, data in ((self.product_name, names),(self.product_color, colors)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)

