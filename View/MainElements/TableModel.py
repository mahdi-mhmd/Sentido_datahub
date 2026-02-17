"""
Table model implementation for Qt table views.
"""
from PySide6.QtCore import Qt, QAbstractTableModel


class TableModel(QAbstractTableModel):
    def __init__(self, headers,data, parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._headers[section]

        return section + 1  # row numbers

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

    def row_data(self, row):
        if 0 <= row < len(self._data):
            return self._data[row]
        return None