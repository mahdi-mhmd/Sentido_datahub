from PySide6.QtCore import QObject,Signal

from View.Pages.EC_Page.EC_Dialogs.ECEditDialog import ECEditDialog
from View.MainElements.MessageDialog import MessageDialog


class ECEditController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,row,model):
        super(ECEditController,self).__init__()
        self.message = None
        self.is_dark = theme
        self.current_row = row
        self.model = model
        self.view = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = ECEditDialog(self.is_dark,types,self.current_row)

        part_numbers, markings, footprints, manufacturers = self.model.fetch_comboboxes_items(self.current_row[0])
        self.view.add_comboboxes_items(part_numbers,markings,footprints,manufacturers)

    def setup_signals(self):
        self.view.edit_requested.connect(self.edit)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def add_comboboxes_items(self, ec_type: str):
        part_numbers, markings, footprints, manufacturers = self.model.fetch_comboboxes_items(ec_type)
        self.view.add_comboboxes_items(part_numbers, markings, footprints, manufacturers)

    def edit(self):
        new_data = [self.none_if_empty(self.view.ec_type.currentText()),
                    self.none_if_empty(self.view.ec_part_number.currentText()),
                    self.none_if_empty(self.view.ec_marking.currentText()),
                    self.none_if_empty(self.view.ec_footprint.currentText()),
                    self.none_if_empty(self.view.ec_manufacturer.currentText()),
                    self.none_if_empty(self.view.ec_qty.value()),
                    self.none_if_empty(self.view.ec_price.value()),
                    self.none_if_empty(self.view.ec_comment.text())]

        result,success = self.model.edit_data(self.current_row,new_data)
        self.message = MessageDialog(self.is_dark, result, success)
        self.message.show()

        self.refresh_requested.emit()

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text
