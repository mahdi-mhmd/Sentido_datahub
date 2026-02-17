from View.Pages.Serial_Page.Serial_Dialogs.SerialSearchDialog import SerialSearchDialog
from Controller.Pages.Serial_Controller.SerialDialogsController.SerialEditController import SerialEditController


class SerialSearchController:

    def __init__(self,theme,model):

        self.is_dark = theme
        self.model = model
        self.view = None
        self.headers = ["Product_Type","Product_Name","Product_Color","Serial","Mac","Status","Comment"]
        self.edit_dialog = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = SerialSearchDialog(self.is_dark, types,self.headers, None)

    def setup_signals(self):
        self.view.adv_search_requested.connect(self.adv_search_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)
        self.view.tableview.row_selected.connect(self.edit_requested)

    def adv_search_requested(self):
        product_type = self.none_if_empty(self.view.product_type.currentText())
        product_name = self.none_if_empty(self.view.product_name.currentText())
        product_color = self.none_if_empty(self.view.product_color.currentText())

        result = self.model.adv_search(product_type,product_name,product_color)
        self.view.tableview.update_data(result)

    def edit_requested(self, data):
        self.edit_dialog = SerialEditController(self.is_dark,data,self.model)
        self.edit_dialog.view.show()
        self.edit_dialog.view.edit_button.clicked.connect(self.adv_search_requested)

    def add_comboboxes_items(self, product_type: str):
        names,colors = self.model.fetch_comboboxes_items(product_type)
        self.view.add_comboboxes_items(names,colors)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

