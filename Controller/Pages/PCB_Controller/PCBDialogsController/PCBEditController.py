from PySide6.QtCore import QObject,Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.PCB_Page.PCB_Dialogs.PCBEditDialog import PCBEditDialog


class PCBEditController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,row,model):
        super(PCBEditController, self).__init__()
        self.message = None
        self.is_dark = theme
        self.current_row = row
        self.model = model
        self.view = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        names = self.model.fetch_distinct_values("Name")
        self.view = PCBEditDialog(self.is_dark,names,self.current_row)

        board_per_sheets, colors, finishings, thicknesses = self.model.fetch_comboboxes_items(self.current_row[0])
        self.view.add_comboboxes_items(board_per_sheets,colors,finishings,thicknesses)

    def setup_signals(self):
        self.view.edit_requested.connect(self.edit)
        self.view.close_requested.connect(self.view.close)
        self.view.name_changed.connect(self.add_comboboxes_items)

    def edit(self):
        new_data = [self.none_if_empty(self.view.pcb_name.currentText()),
                    self.none_if_empty(self.view.pcb_board_per_sheet.currentText()),
                    self.none_if_empty(self.view.pcb_color.currentText()),
                    self.none_if_empty(self.view.pcb_finishing.currentText()),
                    self.none_if_empty(self.view.pcb_thickness.currentText()),
                    self.none_if_empty(self.view.pcb_sheet_qty.value()),
                    self.none_if_empty(self.view.pcb_price.value()),
                    self.none_if_empty(self.view.pcb_comment.text())]

        if new_data[1] is not None:
            new_data[1] = int(new_data[1])

        result,success = self.model.edit_data(self.current_row,new_data)
        self.message = MessageDialog(self.is_dark,result,success)
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
