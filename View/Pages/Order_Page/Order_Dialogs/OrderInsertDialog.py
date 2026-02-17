from PySide6.QtCore import Signal, QSize,QCalendar
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QDateEdit, QLineEdit,QAbstractSpinBox

from View.MainElements.IconPath import icon


class OrderInsertDialog(QDialog):
    insert_requested = Signal()
    close_requested = Signal()
    name_changed = Signal(str)

    def __init__(self, theme, name_list):
        super(OrderInsertDialog, self).__init__()
        self.is_dark = theme
        self.setWindowTitle("Insert (Order)")
        self.setMinimumSize(500, 250)
        self.setMaximumSize(650, 350)

        self.customer_name = QComboBox(self)
        self.customer_tel = QComboBox(self)
        self.customer_city = QComboBox(self)
        self.customer_address = QComboBox(self)

        self.order_date = QDateEdit(self)
        self.order_comment = QLineEdit(self)

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

        if self.is_dark:
            customer_png = icon("Customer_light.png")
            order_png = icon("Order_light.png")
        else:
            customer_png = icon("Customer_dark.png")
            order_png = icon("Order_dark.png")

        self.customer_name.addItems(self.name_list)
        self.customer_name.setCurrentIndex(-1)

        customer_icon = QPushButton()
        customer_icon.setIcon(QIcon(customer_png))

        for combobox, text, num in [(self.customer_name, "Name",1),(self.customer_tel, "Tel",1),
                               (self.customer_city, "City",1),(self.customer_address, "Address",None)]:
            combobox.setEditable(True)
            combobox.setFont(font)
            combobox.setMaxVisibleItems(5)
            v_layout = QVBoxLayout()
            v_layout.addWidget(QLabel(text))
            v_layout.addWidget(combobox)
            if num:
                h_layout.addLayout(v_layout)

        h_layout.setContentsMargins(0,0,0,0)

        main_v_layout = QVBoxLayout()
        main_v_layout.addLayout(h_layout)
        main_v_layout.addLayout(v_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(customer_icon)
        h_layout.addLayout(main_v_layout)
        layout.addLayout(h_layout)

        h_layout = QHBoxLayout()

        order_icon = QPushButton()
        order_icon.setIcon(QIcon(order_png))
        h_layout.addWidget(order_icon)

        self.order_date.setFont(font)
        self.order_date.setDisplayFormat("yyyy/MM/dd")
        self.order_date.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.order_date.setCalendar(QCalendar("persian"))
        self.order_date.setCalendarPopup(True)
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Date"))
        v_layout.addWidget(self.order_date)
        h_layout.addLayout(v_layout,1)

        self.order_comment.setFont(font)
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("Comment"))
        v_layout.addWidget(self.order_comment)
        h_layout.addLayout(v_layout,3)

        layout.addLayout(h_layout)

        for icons in [customer_icon, order_icon]:
            icons.setIconSize(QSize(40, 40))
            icons.setFixedSize(50, 50)
            icons.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }""")

    def setup_buttons(self,layout):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.insert_button)
        h_layout.addWidget(self.close_button)
        h_layout.insertStretch(0, 1)
        layout.addLayout(h_layout)

    def setup_signals(self):
        self.insert_button.clicked.connect(self.insert_requested.emit)
        self.close_button.clicked.connect(self.close_requested.emit)
        self.customer_name.currentIndexChanged.connect(lambda _: self.name_changed.emit(self.customer_name.currentText()))

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
        base_dateedit_style = """
        QDateEdit {
            border: none;
            border-bottom: 2px solid gray;
            padding-right: 18px;
        }
        QDateEdit QLineEdit {
            border: none;
            background: transparent;
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
            theme_dateedit_style = """
            QDateEdit:focus {
                border-bottom: 2px solid #b03b02;
            }"""
            calendar_style = """
            QCalendarWidget {
                background-color: black;
                color: white;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: white;
                color: black;
                padding: 4px;
            }
            QCalendarWidget QToolButton#qt_calendar_monthbutton {
                background-color: white;
                color: black;
                font-weight: bold;
                border: none;
                padding-right: 18px;
                text-align: center;
            }
            QCalendarWidget QToolButton#qt_calendar_monthbutton::menu-indicator {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 10px;
                height: 10px;
                margin-right: 4px;
            }
            QCalendarWidget QToolButton#qt_calendar_yearbutton {
                background-color: white;
                color: black;
                font-weight: bold;
                border: none;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                min-width: 24px;
                min-height: 24px;
                border: none;
            }   
            QCalendarWidget QMenu {
                background-color: black;
                color: white;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #ff6f29;
                selection-color: white;
                gridline-color: #ccc;
            }
            QCalendarWidget QSpinBox::up-button,
            QCalendarWidget QSpinBox::down-button {
                width: 0px;
                height: 0px;
                subcontrol-origin: border;
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
            theme_dateedit_style = """
            QDateEdit:focus {
                border-bottom: 2px solid #ff6f29;
            }"""
            calendar_style = """
            QCalendarWidget {
                background-color: white;
                color: black;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: white;
                color: black;
                padding: 4px;
            }
            QCalendarWidget QToolButton#qt_calendar_monthbutton {
                background-color: white;
                color: black;
                font-weight: bold;
                border: none;
                padding-right: 18px;
                text-align: center;
            }
            QCalendarWidget QToolButton#qt_calendar_monthbutton::menu-indicator {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 10px;
                height: 10px;
                margin-right: 4px;
            }
            QCalendarWidget QToolButton#qt_calendar_yearbutton {
                background-color: white;
                color: black;
                font-weight: bold;
                border: none;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                min-width: 24px;
                min-height: 24px;
                border: none;
            }
            QCalendarWidget QMenu {
                background-color: white;
                color: black;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #ff6f29;
                selection-color: black;
                gridline-color: #ccc;
            }
            QCalendarWidget QSpinBox::up-button,
            QCalendarWidget QSpinBox::down-button {
                width: 0px;
                height: 0px;
                subcontrol-origin: border;
            }"""

        for combobox in [self.customer_name, self.customer_tel,self.customer_city, self.customer_address]:
            combobox.setStyleSheet(base_combobox_style + theme_combobox_style)

        self.order_date.setStyleSheet(base_dateedit_style+theme_dateedit_style)

        self.order_comment.setStyleSheet(base_lineedit_style + theme_lineedit_style)

        calendar = self.order_date.calendarWidget()
        calendar.setStyleSheet(calendar_style)

        self.insert_button.setStyleSheet(base_button_style + theme_button_style)

    def add_comboboxes_items(self, tels, cities,addresses):
        for combobox, data in ((self.customer_tel, tels),(self.customer_city, cities),(self.customer_address, addresses)):
            text = combobox.currentText()
            combobox.clear()
            combobox.addItems(data)
            combobox.setCurrentText(text)
