from View.Pages.EC_Page.EC_Dialogs.ECSearchDialog import ECSearchDialog
from Controller.Pages.EC_Controller.ECDialogsController.ECEditController import ECEditController


class ECSearchController:

    def __init__(self,theme,model):

        self.is_dark = theme
        self.model = model
        self.view = None
        self.headers = ["Type","Part_number","Marking","Footprint","Manufacturer","Quantity","Price","Comment"]
        self.edit_dialog = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = ECSearchDialog(self.is_dark, types,self.headers, None)

    def setup_signals(self):
        self.view.adv_search_requested.connect(self.adv_search_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)
        self.view.tableview.row_selected.connect(self.edit_requested)

    def adv_search_requested(self):
        ec_type = self.none_if_empty(self.view.ec_type.currentText())
        ec_part_number = self.none_if_empty(self.view.ec_part_number.currentText())
        ec_marking = self.none_if_empty(self.view.ec_marking.currentText())
        ec_footprint = self.none_if_empty(self.view.ec_footprint.currentText())
        ec_manufacturer = self.none_if_empty(self.view.ec_manufacturer.currentText())

        result = self.model.adv_search(ec_type,ec_part_number,ec_marking,ec_footprint,ec_manufacturer)
        self.view.tableview.update_data(result)

    def edit_requested(self, data):
        self.edit_dialog = ECEditController(self.is_dark,data,self.model)
        self.edit_dialog.view.show()
        self.edit_dialog.view.edit_button.clicked.connect(self.adv_search_requested)

    def add_comboboxes_items(self, ec_type: str):
        part_numbers,markings,footprints,manufacturers = self.model.fetch_comboboxes_items(ec_type)
        self.view.add_comboboxes_items(part_numbers,markings,footprints,manufacturers)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

