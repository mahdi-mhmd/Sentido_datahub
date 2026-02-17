from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QSpinBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon

from View.MainElements.IconPath import icon


class PCBInsertDialog(QDialog):
    insert_requested = Signal()
    close_requested = Signal()
    name_changed = Signal(str)

    def __init__(self, theme, name_list):
        super(PCBInsertDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Insert (PCB)")
        self.setMinimumSize(700, 250)
        self.setMaximumSize(800, 350)

        self.pcb_name = QComboBox(self)
        self.pcb_board_per_sheet = QComboBox(self)
        self.pcb_color = QComboBox(self)
        self.pcb_finishing = QComboBox(self)
        self.pcb_thickness = QComboBox(self)

        self.pcb_price = QSpinBox(self)
        self.pcb_sheet_qty = QSpinBox(self)
        self.pcb_comment = QLineEdit(self)

        self.insert_button = QPushButton("Insert", self)
        self.close_button = QPushButton("Close", self)

        self.name_list = name_list

        layout = QVBoxLayout(self)
        self.setup_widgets(layout)
        self.setup_buttons(layout)
        self.setup_signals()
        self.setup_style()
        layout.insertStretch(2, 1)

    def setup_widgets(self, layout):
        h_layout = QHBoxLayout()
        font = self.font()
        font.setPointSize(12)

        self.pcb_name.addItems(self.name_list)
        self.pcb_name.setCurrentIndex(-1)

        for combobox, text in [(self.pcb_name, "Name"), (self.pcb_board_per_sheet, "Board/Sheet"), (self.pcb_color, "Color"),
                               (self.pcb_finishing, "Finishing"), (self.pcb_thickness, "Thickness")]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout,1)

        layout.addLayout(h_layout)
        h_layout = QHBoxLayout()

        for spinbox, text, in ((self.pcb_sheet_qty, "Sheet Qty"),
                               (self.pcb_price, "Price")):
            spinbox.setFont(font)
            spinbox.setRange(0, 100000)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(spinbox)
            h_layout.addLayout(v_layout, 1)

        self.pcb_comment.setFont(font)
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Comment"))
        v_layout.addWidget(self.pcb_comment)
        h_layout.addLayout(v_layout, 3)

        layout.addLayout(h_layout)

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.insert_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.insert_button.clicked.connect(self.insert_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.pcb_name.currentIndexChanged.connect(lambda _:self.name_changed.emit(self.pcb_name.currentText()))

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
            self.setWindowIcon(QIcon(icon("Plus_light.png")))
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
            self.setWindowIcon(QIcon(icon("Plus_dark.png")))
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

        for combobox in [self.pcb_name, self.pcb_board_per_sheet, self.pcb_color , self.pcb_finishing, self.pcb_thickness]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        for spinbox in [self.pcb_sheet_qty, self.pcb_price]:
            spinbox.setStyleSheet(base_spinbox_style + theme_spinbox_style)

        self.pcb_comment.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.insert_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self, board_per_sheets, colors, finishings, thicknesses):
        for index in range(len(board_per_sheets)):
            board_per_sheets[index] = str(board_per_sheets[index])

        for combobox, data in ((self.pcb_board_per_sheet, board_per_sheets), (self.pcb_color, colors),
                               (self.pcb_finishing, finishings), (self.pcb_thickness, thicknesses)):
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentIndex(-1)
