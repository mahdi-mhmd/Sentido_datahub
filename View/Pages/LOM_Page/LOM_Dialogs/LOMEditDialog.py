from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QSpinBox

from View.MainElements.IconPath import icon


class LOMEditDialog(QDialog):
    edit_requested = Signal()
    close_requested = Signal()
    ec_type_changed = Signal(str)
    pcb_name_changed = Signal(str)

    def __init__(self, theme, type_list, name_list, feeder_list, nozzle_list, current_data):
        super(LOMEditDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Edit (LOM)")
        self.setMinimumSize(800, 350)
        self.setMaximumSize(800, 450)

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

        self.lom_sign = QLineEdit(self)
        self.lom_feeder = QComboBox(self)
        self.lom_nozzle = QComboBox(self)
        self.lom_count = QSpinBox(self)
        self.lom_comment = QLineEdit(self)

        self.edit_button = QPushButton("Edit", self)
        self.close_button = QPushButton("Close", self)

        self.ec_type_list = type_list
        self.pcb_name_list = name_list
        self.lom_feeder_list = feeder_list
        self.lom_nozzle_list = nozzle_list
        self.current_data = current_data

        layout = QVBoxLayout(self)
        self.setup_widgets(layout)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()
        layout.insertStretch(3, 1)

    def setup_widgets(self, layout):
        h_layout = QHBoxLayout()
        font = self.font()
        font.setPointSize(12)

        if self.is_dark:
            pcb_png = icon("PCB_light.png")
            ec_png = icon("Component_light.png")
            lom_png = icon("LOM_light.png")
        else:
            pcb_png = icon("PCB_dark.png")
            ec_png = icon("Component_dark.png")
            lom_png = icon("LOM_dark.png")

        self.pcb_name.addItems(self.pcb_name_list)

        pcb_icon = QPushButton()
        pcb_icon.setIcon(QIcon(pcb_png))
        h_layout.addWidget(pcb_icon)

        for combobox, text, data in [(self.pcb_name, "Name",self.current_data[0][0]),(self.pcb_board_per_sheet, "Board/Sheet",self.current_data[0][1]),
                                     (self.pcb_color, "Color",self.current_data[0][2]),(self.pcb_finishing, "Finishing",self.current_data[0][3]),
                                     (self.pcb_thickness, "Thickness",self.current_data[0][4])]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setCurrentText(data)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout,1)

        h_layout.setContentsMargins(0, 0, 0, 15)
        layout.addLayout(h_layout)

        self.ec_type.addItems(self.ec_type_list)

        h_layout = QHBoxLayout()
        ec_icon = QPushButton()
        ec_icon.setIcon(QIcon(ec_png))
        h_layout.addWidget(ec_icon)

        for combobox, text, data in [(self.ec_type, "Type",self.current_data[1][0]), (self.ec_part_number, "Part number",self.current_data[1][1]),
                               (self.ec_marking, "Marking",self.current_data[1][2]),(self.ec_footprint, "Footprint",self.current_data[1][3]),
                               (self.ec_manufacturer, "Manufacturer",self.current_data[1][4])]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setCurrentText(data)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout,1)

        h_layout.setContentsMargins(0, 0, 0, 15)
        layout.addLayout(h_layout)

        h_layout = QHBoxLayout()

        for combobox, text, data in ((self.lom_feeder, "Feeder",self.current_data[2][0]), (self.lom_nozzle, "Nozzle",self.current_data[2][1]),):
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setCurrentText(data)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout,1)

        self.lom_count.setFont(font)
        self.lom_count.setRange(0, 100000)
        self.lom_count.setValue(self.current_data[2][2])
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Count"))
        v_layout.addWidget(self.lom_count)
        h_layout.addLayout(v_layout,1)

        v_layout = QVBoxLayout()
        self.lom_sign.setFont(font)
        self.lom_sign.setText(self.current_data[2][3])
        v_layout.addWidget(QLabel("Sign list"))
        v_layout.addWidget(self.lom_sign)
        h_layout.addLayout(v_layout,2)

        self.lom_comment.setFont(font)
        self.lom_comment.setText(self.current_data[2][4])
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(QLabel("Comment"))
        v_layout.addWidget(self.lom_comment)

        h_layout = QHBoxLayout()
        lom_icon = QPushButton()
        lom_icon.setIcon(QIcon(lom_png))
        h_layout.addWidget(lom_icon)

        h_layout.addLayout(v_layout)

        layout.addLayout(h_layout)

        for icons in [pcb_icon, ec_icon, lom_icon]:
            icons.setIconSize(QSize(40, 40))
            icons.setFixedSize(50, 50)
            icons.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }""")

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.edit_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.edit_button.clicked.connect(self.edit_requested.emit)
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

        base_lineedit_style = """
        QLineEdit {
            border: none;
            border-bottom: 2px solid gray;
        }"""
        base_spinbox_style = """
        QSpinBox {
            border: none;
            border-bottom: 2px solid gray;
            padding-right: 15px;
        }
        QSpinBox::up-button, 
        QSpinBox::down-button {
            subcontrol-origin: border;
            width: 0px;
            border: none;
        }
        QSpinBox::up-arrow, 
        QSpinBox::down-arrow {
            image: none;
        }"""

        if self.is_dark:
            self.setWindowIcon(QIcon(icon("Edit_light.png")))
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
            theme_lineedit_style=""" 
            QLineEdit:focus {
                border-bottom: 2px solid #b03b02;
            }"""
            theme_spinbox_style = """
            QSpinBox:focus {
                border-bottom: 2px solid #b03b02;
            }"""

        else:
            self.setWindowIcon(QIcon(icon("Edit_dark.png")))
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
            theme_lineedit_style = """ 
            QLineEdit:focus {
                border-bottom: 2px solid #ff6f29;
            }"""
            theme_spinbox_style = """
            QSpinBox:focus {
                border-bottom: 2px solid #ff6f29;
            }"""

        for combobox in [self.ec_type, self.ec_part_number,self.ec_marking ,self.ec_footprint, self.ec_manufacturer,
                         self.pcb_name, self.pcb_board_per_sheet,self.pcb_color,self.pcb_finishing,self.pcb_thickness,
                         self.lom_feeder,self.lom_nozzle]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)
        for lineedit in [self.lom_sign,self.lom_comment]:
            lineedit.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.lom_count.setStyleSheet(base_spinbox_style + theme_spinbox_style)

        self.edit_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self):
        for combobox, data in ((self.lom_feeder ,self.lom_feeder_list),(self.lom_nozzle , self.lom_nozzle_list)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)

    def add_ec_comboboxes_items(self, part_numbers,markings ,footprints, manufacturers):
        for combobox, data in ((self.ec_part_number, part_numbers), (self.ec_marking, markings),
                               (self.ec_footprint, footprints),(self.ec_manufacturer, manufacturers)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)

    def add_pcb_comboboxes_items(self, board_per_sheets, colors, finishings, thickness):
        for index in range(len(board_per_sheets)):
            board_per_sheets[index] = str(board_per_sheets[index])

        for combobox, data in ((self.pcb_board_per_sheet, board_per_sheets), (self.pcb_color, colors),
                               (self.pcb_finishing, finishings), (self.pcb_thickness, thickness)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)
