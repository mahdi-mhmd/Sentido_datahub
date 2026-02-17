from PySide6.QtWidgets import QVBoxLayout, QWidget

from View.MainElements.Searchbar import Searchbar
from View.MainElements.BasicToolbar import BasicToolbar
from View.MainElements.TableView import TableView


class OrderPageView(QWidget):
    def __init__(self, theme,table_data,search_suggestions):
        super().__init__()

        self.product_layout = QVBoxLayout(self)
        self.searchbar = Searchbar(theme, "Name", search_suggestions)
        self.toolbar = BasicToolbar(theme)
        self.tableview = TableView(theme, ["Name","Tel","City","Address","date","Status","Order_ID","Comment"],table_data)

        self.setup_widgets()

    def setup_widgets(self):
        for widget in [self.searchbar, self.toolbar, self.tableview]:
            self.product_layout.addWidget(widget)
