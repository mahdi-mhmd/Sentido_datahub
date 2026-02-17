"""
Toolbar widget for the EC page.
Buttons:
    - Advanced search
    - Insert component
    - Remove component
"""
from PySide6.QtWidgets import QToolBar, QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

from View.MainElements.IconPath import icon


class BasicToolbar(QToolBar):
    adv_search_requested = Signal()
    insert_requested = Signal()
    remove_requested = Signal()
    refresh_requested = Signal()

    def __init__(self,theme):
        super().__init__()
        self.is_dark = theme

        self.search_button = QToolButton()
        self.insert_button = QToolButton()
        self.remove_button = QToolButton()
        self.edit_button = QToolButton()
        self.refresh_button = QToolButton()

        self.setup_widgets()
        self.setup_signals()
        self.setup_style()

    def setup_widgets(self):
        for btn in [self.search_button,self.insert_button,self.remove_button,self.refresh_button]:
            self.addWidget(btn)
            btn.setFixedSize(33,28)

    def setup_signals(self):
        self.search_button.clicked.connect(self.adv_search_requested.emit)
        self.insert_button.clicked.connect(self.insert_requested.emit)
        self.remove_button.clicked.connect(self.remove_requested.emit)
        self.refresh_button.clicked.connect(self.refresh_requested.emit)

    def setup_style(self):
        base_style = """
        QToolBar {
            background-color: transparent;
            spacing: 5px;
            padding: 0px 0px 0px 5px;
            margin: 0px 0px 0px 0px;
        }
        QToolButton {
            background-color: transparent;  
            border: none;
            padding: 5px 5px;
            border-radius: 5px;   
        }"""

        if self.is_dark:
            for btn, icons in [(self.search_button, QIcon(icon("ADVSearch_light.png"))),
                               (self.insert_button, QIcon(icon("Plus_light.png"))),
                               (self.remove_button, QIcon(icon("Minus_light.png"))),
                               (self.refresh_button, QIcon(icon("Refresh_light.png")))]:
                btn.setIcon(icons)

            theme_style = """
            QToolButton:hover {
                background-color: #b03b02;
            }"""
        else:
            for btn, icons in [(self.search_button, QIcon(icon("ADVSearch_dark.png"))),
                               (self.insert_button, QIcon(icon("Plus_dark.png"))),
                               (self.remove_button, QIcon(icon("Minus_dark.png"))),
                               (self.refresh_button, QIcon(icon("Refresh_dark.png")))]:
                btn.setIcon(icons)
            theme_style = """
            QToolButton:hover {
                background-color: #ff6f29;
            }"""

        self.setStyleSheet(base_style + theme_style)