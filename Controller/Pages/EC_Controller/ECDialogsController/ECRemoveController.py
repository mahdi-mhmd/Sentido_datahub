from PySide6.QtCore import QObject,Signal

from View.Pages.EC_Page.EC_Dialogs.ECRemoveDialog import ECRemoveDialog
from View.MainElements.MessageDialog import MessageDialog


class ECRemoveController(QObject):
    refresh_requested = Signal()

    def __init__(self, theme,model):
        super(ECRemoveController, self).__init__()
        self.is_dark = theme
        self.model = model
        self.view = None
        self.message = None
        self.setup_view()
        self.setup_signals()

        self.error = None

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = ECRemoveDialog(self.is_dark, types)

    def setup_signals(self):
        self.view.remove_requested.connect(self.remove_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def remove_requested(self):
        ec_type = self.none_if_empty(self.view.ec_type.currentText())
        ec_part_number = self.none_if_empty(self.view.ec_part_number.currentText())
        ec_marking = self.none_if_empty(self.view.ec_marking.currentText())
        ec_footprint = self.none_if_empty(self.view.ec_footprint.currentText())
        ec_manufacturer = self.none_if_empty(self.view.ec_manufacturer.currentText())

        result, success = self.model.remove(ec_type, ec_part_number,ec_marking, ec_footprint, ec_manufacturer)

        self.message = MessageDialog(self.is_dark, result, success)
        self.message.show()

        self.refresh_requested.emit()

    def add_comboboxes_items(self, ec_type: str):
        ec_part_numbers,markings,footprints,manufacturers = self.model.fetch_comboboxes_items(ec_type)
        self.view.add_comboboxes_items(ec_part_numbers,markings,footprints,manufacturers)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

