from View.Pages.PCB_Page.PCB_Dialogs.PCBSearchDialog import PCBSearchDialog
from Controller.Pages.PCB_Controller.PCBDialogsController.PCBEditController import PCBEditController


class PCBSearchController:

    def __init__(self,theme,model):

        self.is_dark = theme
        self.model = model
        self.view = None
        self.headers = ["Name","Sheet/Board","Color","Finishing","Thickness","Sheet_Qty","Board_Qty","Price","Comment"]
        self.edit_dialog = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        names = self.model.fetch_distinct_values("Name")
        self.view = PCBSearchDialog(self.is_dark, names,self.headers, None)

    def setup_signals(self):
        self.view.adv_search_requested.connect(self.adv_search_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.name_changed.connect(self.add_comboboxes_items)
        self.view.tableview.row_selected.connect(self.edit_requested)

    def adv_search_requested(self):
        pcb_name = self.none_if_empty(self.view.pcb_name.currentText())
        pcb_board_per_sheet = self.none_if_empty(self.view.pcb_board_per_sheet.currentText())
        pcb_color = self.none_if_empty(self.view.pcb_color.currentText())
        pcb_finishing = self.none_if_empty(self.view.pcb_finishing.currentText())
        pcb_thickness = self.none_if_empty(self.view.pcb_thickness.currentText())

        if pcb_board_per_sheet is not None:
            pcb_board_per_sheet = int(pcb_board_per_sheet)

        result = self.model.adv_search(pcb_name,pcb_board_per_sheet,pcb_color,pcb_finishing,pcb_thickness)
        self.view.tableview.update_data(result)

    def edit_requested(self, data):
        self.edit_dialog = PCBEditController(self.is_dark,data,self.model)
        self.edit_dialog.view.show()
        self.edit_dialog.view.edit_button.clicked.connect(self.adv_search_requested)

    def add_comboboxes_items(self, pcb_name: str):
        board_per_sheets, colors, finishings, thicknesses = self.model.fetch_comboboxes_items(pcb_name)
        self.view.add_comboboxes_items(board_per_sheets, colors, finishings, thicknesses)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

