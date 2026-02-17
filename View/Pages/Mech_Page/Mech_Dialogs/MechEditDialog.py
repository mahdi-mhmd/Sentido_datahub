from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QSpinBox

from View.MainElements.IconPath import icon


class MechEditDialog(QDialog):
    edit_requested = Signal()
    close_requested = Signal()
    type_changed = Signal(str)

    def __init__(self, theme, type_list, current_data):
        super(MechEditDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Edit (Mechanical part)")
        self.setMinimumSize(550, 250)
        self.setMaximumSize(650, 350)

        self.mech_type = QComboBox(self)
        self.mech_name = QComboBox(self)
        self.mech_color = QComboBox(self)
        self.mech_qty = QSpinBox(self)
        self.mech_comment = QLineEdit(self)

        self.edit_button = QPushButton("Edit", self)
        self.close_button = QPushButton("Close", self)

        self.type_list = type_list
        self.current_data = current_data

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

        self.mech_type.addItems(self.type_list)

        for combobox, text, data in [(self.mech_type, "Type", self.current_data[0]),(self.mech_name, "Name", self.current_data[1]),
                                     (self.mech_color, "Color",self.current_data[2])]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            combobox.setCurrentText(data)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            h_layout.addLayout(v_layout,1)

        layout.addLayout(h_layout)
        h_layout = QHBoxLayout()

        self.mech_qty.setFont(font)
        self.mech_qty.setRange(0, 100000)
        self.mech_qty.setValue(self.current_data[3])
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Qty"))
        v_layout.addWidget(self.mech_qty)
        h_layout.addLayout(v_layout, 1)

        self.mech_comment.setFont(font)
        self.mech_comment.setText(self.current_data[4])
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Comment"))
        v_layout.addWidget(self.mech_comment)
        h_layout.addLayout(v_layout, 4)

        layout.addLayout(h_layout)

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.edit_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.edit_button.clicked.connect(self.edit_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.mech_type.currentIndexChanged.connect(lambda _: self.type_changed.emit(self.mech_type.currentText()))

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
            height: 2px;
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

        for combobox in [self.mech_type, self.mech_name,self.mech_color]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        self.mech_qty.setStyleSheet(base_spinbox_style + theme_spinbox_style)

        self.mech_comment.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        self.edit_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self, names, colors):
        for combobox, data in ((self.mech_name, names),(self.mech_color, colors)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)