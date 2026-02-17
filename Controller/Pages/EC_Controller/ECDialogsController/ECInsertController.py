from PySide6.QtCore import QObject, Signal

from View.Pages.EC_Page.EC_Dialogs.ECInsertDialog import ECInsertDialog
from View.MainElements.MessageDialog import MessageDialog


class ECInsertController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,model):
        super(ECInsertController,self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = ECInsertDialog(self.is_dark, types)

    def setup_signals(self):
        self.view.insert_requested.connect(self.insert_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def insert_requested(self):
        ec_type = self.none_if_empty(self.view.ec_type.currentText())
        ec_part_number = self.none_if_empty(self.view.ec_part_number.currentText())
        ec_marking = self.none_if_empty(self.view.ec_marking.currentText())
        ec_footprint = self.none_if_empty(self.view.ec_footprint.currentText())
        ec_manufacturer = self.none_if_empty(self.view.ec_manufacturer.currentText())
        ec_quantity = self.none_if_empty(self.view.ec_qty.value())
        ec_price = self.none_if_empty(self.view.ec_price.value())
        ec_comment = self.none_if_empty(self.view.ec_comment.text())

        if ec_type is None or ec_part_number is None:
            self.message = MessageDialog(self.is_dark, "Please fill the required fields", 0)
            self.message.show()
            return

        result, success = self.model.insert(ec_type,ec_part_number,ec_marking,ec_footprint,ec_manufacturer,ec_quantity,ec_price,ec_comment)
        self.message = MessageDialog(self.is_dark, result, success)
        self.message.show()

        self.refresh_requested.emit()
        
    def add_comboboxes_items(self, ec_type: str):
        part_numbers, markings, footprints, manufacturers = self.model.fetch_comboboxes_items(ec_type)
        self.view.add_comboboxes_items(part_numbers, markings, footprints, manufacturers)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

