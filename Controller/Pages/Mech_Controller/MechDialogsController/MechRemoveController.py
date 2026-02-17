from PySide6.QtCore import QObject,Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.Mech_Page.Mech_Dialogs.MechRemoveDialog import MechRemoveDialog


class MechRemoveController(QObject):
    refresh_requested = Signal()

    def __init__(self, theme,model):
        super(MechRemoveController, self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.setup_view()
        self.setup_signals()

        self.error = None

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = MechRemoveDialog(self.is_dark, types)

    def setup_signals(self):
        self.view.remove_requested.connect(self.remove_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def remove_requested(self):
        mech_type = self.none_if_empty(self.view.mech_type.currentText())
        mech_name = self.none_if_empty(self.view.mech_name.currentText())
        mech_color = self.none_if_empty(self.view.mech_color.currentText())

        result,success = self.model.remove(mech_type, mech_name,mech_color)
        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()

        self.refresh_requested.emit()

    def add_comboboxes_items(self, mech_type: str):
        names,colors = self.model.fetch_comboboxes_items(mech_type)
        self.view.add_comboboxes_items(names,colors)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

