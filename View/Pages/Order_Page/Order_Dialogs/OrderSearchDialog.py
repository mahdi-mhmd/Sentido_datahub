from PySide6.QtCore import Signal,QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel

from View.MainElements.TableView import TableView
from View.MainElements.IconPath import icon


class OrderSearchDialog(QDialog):
    adv_search_requested = Signal()
    close_requested = Signal()
    name_changed = Signal(str)

    def __init__(self, theme, name_list, headers, info):
        super(OrderSearchDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Search (Order)")
        self.setMinimumSize(700, 300)

        self.customer_name = QComboBox(self)
        self.customer_tel = QComboBox(self)
        self.customer_city = QComboBox(self)

        self.search_button = QPushButton("Search", self)
        self.close_button = QPushButton("Close", self)

        self.tableview = TableView(self.is_dark,headers,info)

        self.name_list = name_list

        layout = QVBoxLayout(self)
        self.setup_widgets(layout)
        layout.addWidget(self.tableview)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()
        layout.insertStretch(2, 1)

    def setup_widgets(self, layout):
        h_layout = QHBoxLayout()
        font = self.font()
        font.setPointSize(12)

        self.customer_name.addItems(self.name_list)
        self.customer_name.setCurrentIndex(-1)

        for combobox, text in [(self.customer_name, "Name"),(self.customer_tel, "Tel"),(self.customer_city, "City")]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setFixedSize(QSize(130, 27))
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout)
        h_layout.addStretch()

        layout.addLayout(h_layout)

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.search_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.search_button.clicked.connect(self.adv_search_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.customer_name.currentIndexChanged.connect(lambda _: self.name_changed.emit(self.customer_name.currentText()))

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

        for combobox in [self.customer_name, self.customer_tel,self.customer_city]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        self.search_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self, tels, cities):
        for combobox, data in ((self.customer_tel, tels),(self.customer_city, cities)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)
