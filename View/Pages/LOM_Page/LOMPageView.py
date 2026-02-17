from PySide6.QtWidgets import QVBoxLayout, QWidget

from View.MainElements.Searchbar import Searchbar
from View.MainElements.BasicToolbar import BasicToolbar
from View.MainElements.TableView import TableView


class LOMPageView(QWidget):
    def __init__(self, theme,table_data,search_suggestions):
        super().__init__()

        self.lom_layout = QVBoxLayout(self)
        self.searchbar = Searchbar(theme, "PCB Name", search_suggestions)
        self.toolbar = BasicToolbar(theme)
        self.tableview = TableView(theme, ["PCB-Name","PCB-B/S","EC-PN","EC-Footprint","EC-Manufacturer","Feeder","Nozzle","Count","Sign list","Comment","PCB_ID","EC_ID"],table_data)
        self.setup_widgets()

    def setup_widgets(self):
        for widget in [self.searchbar, self.toolbar, self.tableview]:
            self.lom_layout.addWidget(widget)
