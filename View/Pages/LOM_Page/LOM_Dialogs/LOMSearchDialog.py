from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel

from View.MainElements.TableView import TableView
from View.MainElements.IconPath import icon


class LOMSearchDialog(QDialog):
    search_requested = Signal()
    close_requested = Signal()
    ec_type_changed = Signal(str)
    pcb_name_changed = Signal(str)

    def __init__(self, theme, type_list, name_list, headers, info):
        super(LOMSearchDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("ADV Search (LOM)")
        self.setMinimumSize(700, 300)

        self.ec_type = QComboBox(self)
        self.ec_part_number = QComboBox(self)
        self.ec_marking = QComboBox(self)
        self.ec_footprint = QComboBox(self)
        self.ec_manufacturer = QComboBox(self)

        self.pcb_name = QComboBox(self)
        self.pcb_board_per_sheet = QComboBox(self)
        self.pcb_color = QComboBox(self)
        self.pcb_finishing = QComboBox(self)
        self.pcb_thickness = QComboBox(self)

        self.search_button = QPushButton("Search", self)
        self.close_button = QPushButton("Close", self)

        self.tableview = TableView(self.is_dark,headers,info)

        self.ec_type_list = type_list
        self.pcb_name_list = name_list

        layout = QVBoxLayout(self)
        self.setup_widgets(layout)
        layout.addWidget(self.tableview)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()
        layout.insertStretch(3, 1)

    def setup_widgets(self, layout):
        h_layout = QHBoxLayout()

        font = self.font()
        font.setPointSize(12)

        self.pcb_name.addItems(self.pcb_name_list)
        self.pcb_name.setCurrentIndex(-1)

        if self.is_dark:
            pcb_png = icon("PCB_light.png")
            ec_png = icon("Component_light.png")
        else:
            pcb_png = icon("PCB_dark.png")
            ec_png = icon("Component_dark.png")

        pcb_icon = QPushButton()
        pcb_icon.setIcon(QIcon(icon(pcb_png)))
        h_layout.addWidget(pcb_icon)

        for combobox, text in [(self.pcb_name, "Name"), (self.pcb_board_per_sheet, "Board/Sheet"),
                               (self.pcb_color, "Color"),
                               (self.pcb_finishing, "Finishing"), (self.pcb_thickness, "Thickness")]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setFixedSize(QSize(130,27))
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout)

        h_layout.addStretch()
        h_layout.setContentsMargins(0, 0, 0, 15)
        layout.addLayout(h_layout)

        self.ec_type.addItems(self.ec_type_list)
        self.ec_type.setCurrentIndex(-1)

        h_layout = QHBoxLayout()

        ec_icon = QPushButton()
        ec_icon.setIcon(QIcon(icon(ec_png)))
        h_layout.addWidget(ec_icon)

        for combobox, text in [(self.ec_type, "Type"), (self.ec_part_number, "Part number"),
                               (self.ec_marking, "Marking"),
                               (self.ec_footprint, "Footprint"), (self.ec_manufacturer, "Manufacturer")]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setFixedSize(QSize(130,27))
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout)

        h_layout.addStretch()
        h_layout.setContentsMargins(0, 0, 0, 15)
        layout.addLayout(h_layout)

        for icons in [pcb_icon, ec_icon]:
            icons.setIconSize(QSize(40, 40))
            icons.setFixedSize(50, 50)
            icons.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }""")


    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.search_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.search_button.clicked.connect(self.search_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.ec_type.currentIndexChanged.connect(lambda _:self.ec_type_changed.emit(self.ec_type.currentText()))
        self.pcb_name.currentIndexChanged.connect(lambda _: self.pcb_name_changed.emit(self.pcb_name.currentText()))

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

        for combobox in [self.ec_type, self.ec_part_number,self.ec_marking ,self.ec_footprint, self.ec_manufacturer,
                         self.pcb_name, self.pcb_board_per_sheet,self.pcb_color,self.pcb_finishing,self.pcb_thickness]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        self.search_button.setStyleSheet(base_button_style + theme_button_style)

    def add_ec_comboboxes_items(self, part_numbers,markings ,footprints, manufacturers):
        for combobox, data in ((self.ec_part_number, part_numbers), (self.ec_marking, markings),
                               (self.ec_footprint, footprints),(self.ec_manufacturer, manufacturers)):
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentIndex(-1)

    def add_pcb_comboboxes_items(self, board_per_sheets, colors, finishings, thickness):
        for index in range(len(board_per_sheets)):
            board_per_sheets[index] = str(board_per_sheets[index])

        for combobox, data in ((self.pcb_board_per_sheet, board_per_sheets), (self.pcb_color, colors),
                               (self.pcb_finishing, finishings), (self.pcb_thickness, thickness)):
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentIndex(-1)