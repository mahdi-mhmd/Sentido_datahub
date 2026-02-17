from Model.Pages.OrderDtlPageModel import OrderDtlPageModel
from View.Pages.Order_Page.Order_Dialogs.OrderDtlDialog import OrderDtlDialog

from Controller.Pages.Order_Controller.OrderDialogsController.OrderDtlDialogsController.OrderDtlInsertController import OrderDtlInsertController
from Controller.Pages.Order_Controller.OrderDialogsController.OrderDtlDialogsController.OrderDtlRemoveController import OrderDtlRemoveController
from Controller.Pages.Order_Controller.OrderDialogsController.OrderDtlDialogsController.OrderDtlSearchController import OrderDtlSearchController


class OrderDtlPageController:
    def __init__(self,theme,order_id,current_status):
        self.is_dark = theme
        self.view = None
        self.model = OrderDtlPageModel()

        self.order_id = order_id
        self.current_status = current_status
        self.table_data = None
        self.remove_dialog = None
        self.insert_dialog = None
        self.adv_search_dialog = None
        self.edit_dialog = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        self.table_data = self.model.fetch_order_data(self.order_id)
        suggestions = self.model.fetch_suggestions(self.order_id)
        self.view = OrderDtlDialog(self.is_dark,self.table_data,suggestions,self.current_status)

    def setup_signals(self):
        self.view.toolbar.adv_search_requested.connect(self.adv_search_requested)
        self.view.toolbar.insert_requested.connect(self.insert_requested)
        self.view.toolbar.remove_requested.connect(self.remove_requested)
        self.view.toolbar.refresh_requested.connect(self.refresh)
        self.view.searchbar.search_requested.connect(self.search_requested)
        self.view.searchbar.text_changed.connect(self.text_cleared)
        self.view.searchbar.suggestion_selected.connect(self.suggestion_selected)
        self.view.status_changed.connect(self.change_status)

    def adv_search_requested(self):
        self.adv_search_dialog = OrderDtlSearchController(self.is_dark,self.model,self.order_id)
        self.adv_search_dialog.view.show()

    def insert_requested(self):
        self.insert_dialog = OrderDtlInsertController(self.is_dark,self.model,self.order_id)
        self.insert_dialog.view.show()
        self.insert_dialog.refresh_requested.connect(self.refresh)

    def remove_requested(self):
        self.remove_dialog = OrderDtlRemoveController(self.is_dark,self.model,self.order_id)
        self.remove_dialog.view.show()
        self.remove_dialog.refresh_requested.connect(self.refresh)

    def refresh(self):
        self.table_data = self.model.fetch_order_data(self.order_id)
        self.view.tableview.update_data(self.table_data)
        self.view.searchbar.lineedit.clear()
        suggestions = self.model.fetch_distinct_values("Name")
        self.view.searchbar.update_suggestions(suggestions)

    def search_requested(self):
        value = self.view.searchbar.lineedit.text()
        if value == "":
            return
        result = self.model.search(value)
        self.view.tableview.update_data(result)

    def text_cleared(self, value: str):
        if value == "":
            self.view.tableview.update_data(self.table_data)

    def suggestion_selected(self):
        value = self.view.searchbar.lineedit.text()
        result = self.model.search(value)
        self.view.tableview.update_data(result)

    def change_status(self,status):
        self.model.change_status(self.order_id,status)
