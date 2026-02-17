from PySide6.QtCore import QObject, Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.Mech_Page.Mech_Dialogs.MechInsertDialog import MechInsertDialog


class MechInsertController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,model):
        super(MechInsertController,self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = MechInsertDialog(self.is_dark, types)

    def setup_signals(self):
        self.view.insert_requested.connect(self.insert_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def insert_requested(self):
        mech_type = self.none_if_empty(self.view.mech_type.currentText())
        mech_name = self.none_if_empty(self.view.mech_name.currentText())
        mech_color = self.none_if_empty(self.view.mech_color.currentText())
        mech_quantity = self.none_if_empty(self.view.mech_qty.value())
        mech_comment = self.none_if_empty(self.view.mech_comment.text())

        if mech_type is None and mech_name is None:
            self.message = MessageDialog(self.is_dark, "Please fill the required fields", 0)
            self.message.show()
            return

        result,success = self.model.insert(mech_type,mech_name,mech_color,mech_quantity,mech_comment)
        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()

        self.refresh_requested.emit()

    def add_comboboxes_items(self, mech_type: str):
        names, colors = self.model.fetch_comboboxes_items(mech_type)
        self.view.add_comboboxes_items(names,colors)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

