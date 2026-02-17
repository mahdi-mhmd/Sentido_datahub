from View.Pages.Mech_Page.Mech_Dialogs.MechSearchDialog import MechSearchDialog
from Controller.Pages.Mech_Controller.MechDialogsController.MechEditController import MechEditController


class MechSearchController:

    def __init__(self,theme,model):

        self.is_dark = theme
        self.model = model
        self.view = None
        self.headers = ["Type","Name","Color","Qty","Comment"]
        self.edit_dialog = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = MechSearchDialog(self.is_dark, types,self.headers, None)

    def setup_signals(self):
        self.view.adv_search_requested.connect(self.adv_search_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)
        self.view.tableview.row_selected.connect(self.edit_requested)

    def adv_search_requested(self):
        mech_type = self.none_if_empty(self.view.mech_type.currentText())
        mech_name = self.none_if_empty(self.view.mech_name.currentText())
        mech_color = self.none_if_empty(self.view.mech_color.currentText())

        result = self.model.adv_search(mech_type,mech_name,mech_color)
        self.view.tableview.update_data(result)

    def edit_requested(self, data):
        self.edit_dialog = MechEditController(self.is_dark,data,self.model)
        self.edit_dialog.view.show()
        self.edit_dialog.view.edit_button.clicked.connect(self.adv_search_requested)

    def add_comboboxes_items(self, mech_type: str):
        names,colors = self.model.fetch_comboboxes_items(mech_type)
        self.view.add_comboboxes_items(names,colors)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

