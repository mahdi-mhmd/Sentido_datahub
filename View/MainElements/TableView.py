"""
Table view widget for displaying electronic component data.
This view displays component information using a QAbstractTableModel implementation and applies theme-aware styling.
It does not contain any business logic or data manipulation
"""
from PySide6.QtWidgets import QTableView
from PySide6.QtCore import Qt,Signal

from View.MainElements.TableModel import TableModel


class TableView(QTableView):
    row_selected = Signal(object)

    def __init__(self, theme,headers,info=None):
        super().__init__()
        self.is_dark = theme

        if info is None: info = []
        self.table_model = TableModel(headers,info)

        self.setModel(self.table_model)
        self.setup_style()
        self.setup_signal()
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(QTableView.SingleSelection)

    def update_data(self, new_data):
        self.clearSelection()
        self.table_model.update_data(new_data)

    def setup_signal(self):
        self.doubleClicked.connect(self.get_selected_row_data)

    def get_selected_row_data(self,index):
        data = self.table_model.row_data(index.row())
        self.row_selected.emit(data)

    def setup_style(self):
        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = self.font()
        font.setPointSize(13)
        self.setFont(font)

        base_style = """
        QTableView {
            outline: none;              
        }
        QTableView::item {
             padding: 5px;
        }
        QTableView::item:focus {
            border: none;            
            outline: none;
        }"""

        if self.is_dark:
            theme_style = """
            QTableView::item:selected {
                background-color: #b03b02;
                color: white;              
            }"""
        else:
            theme_style = """
            QTableView::item:selected {
                background-color: #ff6f29; 
                color: black;             
            }"""

        self.setStyleSheet(base_style + theme_style)
