from PySide6.QtWidgets import QVBoxLayout, QWidget

from View.MainElements.Searchbar import Searchbar
from View.MainElements.BasicToolbar import BasicToolbar
from View.MainElements.TableView import TableView


class SerialPageView(QWidget):
    def __init__(self, theme,table_data,search_suggestions):
        super().__init__()

        self.serial_layout = QVBoxLayout(self)
        self.searchbar = Searchbar(theme, "Serial", search_suggestions)
        self.toolbar = BasicToolbar(theme)
        self.tableview = TableView(theme, ["Product_Type","Product_Name","Product_Color","Serial","Mac","Status","Comment"],table_data)

        self.setup_widgets()

    def setup_widgets(self):
        for widget in [self.searchbar, self.toolbar, self.tableview]:
            self.serial_layout.addWidget(widget)
