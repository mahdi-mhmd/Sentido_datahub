from PySide6.QtCore import QObject, Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.PCB_Page.PCB_Dialogs.PCBInsertDialog import PCBInsertDialog


class PCBInsertController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,model):
        super(PCBInsertController, self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Name")
        self.view = PCBInsertDialog(self.is_dark, types)

    def setup_signals(self):
        self.view.insert_requested.connect(self.insert_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.name_changed.connect(self.add_comboboxes_items)

    def insert_requested(self):
        pcb_name = self.none_if_empty(self.view.pcb_name.currentText())
        pcb_board_per_sheet = self.none_if_empty(self.view.pcb_board_per_sheet.currentText())
        pcb_color = self.none_if_empty(self.view.pcb_color.currentText())
        pcb_finishing = self.none_if_empty(self.view.pcb_finishing.currentText())
        pcb_thickness = self.none_if_empty(self.view.pcb_thickness.currentText())
        pcb_sheet_qty = self.none_if_empty(self.view.pcb_sheet_qty.value())
        pcb_price = self.none_if_empty(self.view.pcb_price.value())
        pcb_comment = self.none_if_empty(self.view.pcb_comment.text())

        if pcb_name is None or pcb_board_per_sheet is None:
            self.message = MessageDialog(self.is_dark, "Please fill the required fields", 0)
            self.message.show()
            return
        pcb_board_per_sheet = int(pcb_board_per_sheet)

        result,success = self.model.insert(pcb_name,pcb_board_per_sheet,pcb_color,pcb_finishing,pcb_thickness,pcb_sheet_qty,pcb_price,pcb_comment)
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

