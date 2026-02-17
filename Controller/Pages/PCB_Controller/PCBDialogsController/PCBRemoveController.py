from PySide6.QtCore import QObject,Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.PCB_Page.PCB_Dialogs.PCBRemoveDialog import PCBRemoveDialog


class PCBRemoveController(QObject):
    refresh_requested = Signal()

    def __init__(self, theme,model):
        super(PCBRemoveController, self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.setup_view()
        self.setup_signals()

        self.error = None

    def setup_view(self):
        names = self.model.fetch_distinct_values("Name")
        self.view = PCBRemoveDialog(self.is_dark, names)

    def setup_signals(self):
        self.view.remove_requested.connect(self.remove_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.name_changed.connect(self.add_comboboxes_items)

    def remove_requested(self):
        pcb_name = self.none_if_empty(self.view.pcb_name.currentText())
        pcb_board_per_sheet = self.none_if_empty(self.view.pcb_board_per_sheet.currentText())
        pcb_color = self.none_if_empty(self.view.pcb_color.currentText())
        pcb_finishing = self.none_if_empty(self.view.pcb_finishing.currentText())
        pcb_thickness = self.none_if_empty(self.view.pcb_thickness.currentText())

        if pcb_board_per_sheet is not None:
            pcb_board_per_sheet = int(pcb_board_per_sheet)

        result,success = self.model.remove(pcb_name, pcb_board_per_sheet,pcb_color, pcb_finishing, pcb_thickness)
        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()

        self.refresh_requested.emit()

    def add_comboboxes_items(self, pcb_name: str):
        board_per_sheets, colors, finishings, thicknesses = self.model.fetch_comboboxes_items(pcb_name)
        self.view.add_comboboxes_items(board_per_sheets, colors, finishings, thicknesses)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

