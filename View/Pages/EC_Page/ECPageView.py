from PySide6.QtWidgets import QVBoxLayout, QWidget

from View.MainElements.Searchbar import Searchbar
from View.MainElements.BasicToolbar import BasicToolbar
from View.MainElements.TableView import TableView


class ECPageView(QWidget):
    def __init__(self, theme,table_data,search_suggestions):
        super().__init__()

        self.ec_layout = QVBoxLayout(self)
        self.searchbar = Searchbar(theme, "Part number", search_suggestions)
        self.toolbar = BasicToolbar(theme)
        self.tableview = TableView(theme, ["Type","Part_number","Marking","Footprint","Manufacturer","Quantity","Price","Comment"],table_data)

        self.setup_widgets()

    def setup_widgets(self):
        for widget in [self.searchbar, self.toolbar, self.tableview]:
            self.ec_layout.addWidget(widget)
