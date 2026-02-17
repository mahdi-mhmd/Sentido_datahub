from PySide6.QtCore import QObject, Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.Serial_Page.Serial_Dialogs.SerialInsertDialog import SerialInsertDialog


class SerialInsertController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,model):
        super(SerialInsertController,self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = SerialInsertDialog(self.is_dark, types)

    def setup_signals(self):
        self.view.insert_requested.connect(self.insert_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def insert_requested(self):
        product_type = self.none_if_empty(self.view.product_type.currentText())
        product_name = self.none_if_empty(self.view.product_name.currentText())
        product_color = self.none_if_empty(self.view.product_color.currentText())
        serial_serial = self.none_if_empty(self.view.serial_serial.text())
        serial_mac = self.none_if_empty(self.view.serial_mac.text())
        serial_comment = self.none_if_empty(self.view.serial_comment.text())

        if product_type is None and product_name is None and serial_serial is None:
            self.message = MessageDialog(self.is_dark, "Please fill the required fields", 0)
            self.message.show()
            return

        result,success = self.model.insert(product_type,product_name,product_color,serial_serial,serial_mac,serial_comment)
        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()

        self.refresh_requested.emit()

    def add_comboboxes_items(self, product_type: str):
        names, colors = self.model.fetch_comboboxes_items(product_type)
        self.view.add_comboboxes_items(names,colors)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

