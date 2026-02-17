from PySide6.QtCore import QObject,Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.Serial_Page.Serial_Dialogs.SerialEditDialog import SerialEditDialog


class SerialEditController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,row,model):
        super(SerialEditController,self).__init__()
        self.is_dark = theme
        self.current_row = row
        self.model = model
        self.view = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = SerialEditDialog(self.is_dark,types,self.current_row)

        names, colors = self.model.fetch_comboboxes_items(self.current_row[0])
        self.view.add_comboboxes_items(names,colors)

    def setup_signals(self):
        self.view.edit_requested.connect(self.edit)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def add_comboboxes_items(self, product_type: str):
        names, colors = self.model.fetch_comboboxes_items(product_type)
        self.view.add_comboboxes_items(names,colors)

    def edit(self):
        new_data = [(self.none_if_empty(self.view.product_type.currentText()),
                    self.none_if_empty(self.view.product_name.currentText()),
                    self.none_if_empty(self.view.product_color.currentText())),
                    (self.none_if_empty(self.view.serial_serial.text()),
                    self.none_if_empty(self.view.serial_mac.text()),
                    self.none_if_empty(self.view.serial_status.currentText()),
                    self.none_if_empty(self.view.serial_comment.text()))]

        result , success = self.model.edit_data(self.current_row,new_data)
        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()

        self.refresh_requested.emit()

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text
