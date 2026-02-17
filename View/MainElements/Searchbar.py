"""
Search bar widget for the EC page.
This widget combines a QLineEdit and a QPushButton with a search icon, styled to be transparent and visually integrated.
The QLineEdit includes a clear button, and the layout ensures proper spacing and alignment.
"""
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLineEdit, QPushButton, QWidget, QHBoxLayout, QCompleter
from PySide6.QtCore import Qt, Signal, QStringListModel

from View.MainElements.IconPath import icon


class Searchbar(QWidget):
    search_requested = Signal()
    text_changed = Signal(str)
    suggestion_selected = Signal()

    def __init__(self,theme,placeholder,suggestions):
        super().__init__()
        self.is_dark = theme
        self.placeholder = placeholder

        self.lineedit = QLineEdit()
        self.search_button = QPushButton()

        self.completer_model = QStringListModel(suggestions)
        self.completer = QCompleter(self.completer_model, self.lineedit)

        self.setup_widgets(suggestions)
        self.setup_signals()
        self.setup_layout()
        self.setup_style()

    def setup_widgets(self,suggestions):
        self.lineedit.setPlaceholderText(self.placeholder)
        self.lineedit.setClearButtonEnabled(True)
        self.lineedit.setFixedSize(150, 30)

        font = self.font()
        font.setPointSize(12)
        self.lineedit.setFont(font)

        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineedit.setCompleter(self.completer)

    def setup_signals(self):
        self.search_button.clicked.connect(lambda _:self.search_requested.emit())
        self.lineedit.textChanged.connect(lambda _:self.text_changed.emit(self.lineedit.text()))
        self.lineedit.completer().activated.connect(lambda _:self.suggestion_selected.emit())

    def setup_layout(self):
        searchbar_widget = QWidget()
        searchbar_layout = QHBoxLayout(searchbar_widget)
        searchbar_layout.setContentsMargins(0, 0, 0, 0)
        searchbar_layout.setSpacing(0)
        searchbar_layout.addWidget(self.search_button)
        searchbar_layout.addWidget(self.lineedit)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(searchbar_widget)
        main_layout.setContentsMargins(6, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.insertStretch(1, 1)

        if self.is_dark:
            searchbar_widget.setStyleSheet("""
            QWidget {
                border:1px solid white; 
                padding: 3px;
                border-radius: 5px;
                }""")
        else:
            searchbar_widget.setStyleSheet("""
            QWidget {
                border:1px solid black; 
                padding: 3px;
                border-radius: 5px;
                }""")

    def setup_style(self):
        if self.is_dark:
            self.search_button.setIcon(QIcon(icon("Search_light.png")))
        else:
            self.search_button.setIcon(QIcon(icon("Search_dark.png")))

        self.lineedit.setStyleSheet("""
        QLineEdit {
            border:none;
            background:transparent; 
        }""")

        self.search_button.setStyleSheet("""
        QPushButton { 
            border:none;
            background:transparent;
        }""")

    def update_suggestions(self, suggestions: list[str]):
        self.completer_model.setStringList(suggestions)