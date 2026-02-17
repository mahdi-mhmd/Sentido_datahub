from PySide6.QtCore import QObject,Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.Serial_Page.Serial_Dialogs.SerialRemoveDialog import SerialRemoveDialog


class SerialRemoveController(QObject):
    refresh_requested = Signal()

    def __init__(self, theme,model):
        super(SerialRemoveController, self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.setup_view()
        self.setup_signals()

        self.error = None

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = SerialRemoveDialog(self.is_dark, types)

    def setup_signals(self):
        self.view.remove_requested.connect(self.remove_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def remove_requested(self):
        product_type = self.none_if_empty(self.view.product_type.currentText())
        product_name = self.none_if_empty(self.view.product_name.currentText())
        product_color = self.none_if_empty(self.view.product_color.currentText())
        serial_serial = self.none_if_empty(self.view.serial_serial.text())

        result,success = self.model.remove(product_type, product_name,product_color, serial_serial)
        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()

        self.refresh_requested.emit()

    def add_comboboxes_items(self, product_type: str):
        names,colors = self.model.fetch_comboboxes_items(product_type)
        self.view.add_comboboxes_items(names,colors)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

