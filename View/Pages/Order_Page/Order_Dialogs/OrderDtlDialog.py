from PySide6.QtWidgets import QVBoxLayout, QDialog, QComboBox, QHBoxLayout
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

from View.MainElements.IconPath import icon
from View.MainElements.Searchbar import Searchbar
from View.MainElements.BasicToolbar import BasicToolbar
from View.MainElements.TableView import TableView


class OrderDtlDialog(QDialog):
    status_changed = Signal(str)

    def __init__(self, theme,table_data,search_suggestions,current_status):
        super().__init__()
        self.is_dark = theme
        self.setWindowTitle("Order details")
        self.setMinimumSize(700, 300)
        self.orderdtl_layout = QVBoxLayout(self)
        self.searchbar = Searchbar(self.is_dark, "Serial", search_suggestions)
        self.toolbar = BasicToolbar(self.is_dark)
        self.order_status = QComboBox(self)
        self.tableview = TableView(self.is_dark, ["Product_Type","Product_Name","Product_Color","Serial","Count","Unit price"],table_data)
        self.setup_widgets()
        self.setup_combobox(current_status)

    def setup_widgets(self):
        self.orderdtl_layout.addWidget(self.searchbar)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.toolbar)
        h_layout.addWidget(self.order_status)
        h_layout.insertStretch(2,1)
        self.orderdtl_layout.addLayout(h_layout)
        self.orderdtl_layout.addWidget(self.tableview)

    def setup_combobox(self,status):
        font = self.font()
        font.setPointSize(12)
        self.order_status.setFont(font)

        self.order_status.addItems(["Pending","Completed","Cancelled"])
        self.order_status.setCurrentText(status)
        base_combobox_style = """
        QComboBox {
            padding-right: 5px;
            padding-left: 5px;
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
        if self.is_dark:
            self.setWindowIcon(QIcon(icon("OpenBox_light.png")))
            theme_combobox_style = """
            QComboBox:focus {
            border-bottom: 2px solid #b03b02; 
            }
            QComboBox QLineEdit:focus {
            border-bottom: 2px solid #b03b02;
            }"""
        else:
            self.setWindowIcon(QIcon(icon("OpenBox_light.png")))
            theme_combobox_style = """
            QComboBox:focus {
            border-bottom: 2px solid #ff6f29; 
            }
            QComboBox QLineEdit:focus {
            border-bottom: 2px solid #ff6f29;
            }"""
        self.order_status.setStyleSheet(base_combobox_style + theme_combobox_style)

        self.order_status.currentIndexChanged.connect(lambda _: self.status_changed.emit(self.order_status.currentText()))
