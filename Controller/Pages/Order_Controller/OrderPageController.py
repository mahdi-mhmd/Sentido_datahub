from View.Pages.Order_Page.OrderPageView import OrderPageView
from Model.Pages.OrderPageModel import OrderPageModel

from Controller.Pages.Order_Controller.OrderDialogsController.OrderSearchController import OrderSearchController
from Controller.Pages.Order_Controller.OrderDialogsController.OrderInsertController import OrderInsertController
from Controller.Pages.Order_Controller.OrderDialogsController.OrderRemoveController import OrderRemoveController
from Controller.Pages.Order_Controller.OrderDialogsController.OrderDtlPageController import OrderDtlPageController


class OrderPageController:
    def __init__(self,theme):
        self.details_dialog = None
        self.is_dark = theme
        self.view = None
        self.model = OrderPageModel()

        self.table_data = None
        self.remove_dialog = None
        self.insert_dialog = None
        self.adv_search_dialog = None
        self.edit_dialog = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        self.table_data = self.model.fetch_all_data()
        suggestions = self.model.fetch_distinct_values("Name")
        self.view = OrderPageView(self.is_dark,self.table_data,suggestions)

    def setup_signals(self):
        self.view.toolbar.adv_search_requested.connect(self.adv_search_requested)
        self.view.toolbar.insert_requested.connect(self.insert_requested)
        self.view.toolbar.remove_requested.connect(self.remove_requested)
        self.view.toolbar.refresh_requested.connect(self.refresh)
        self.view.searchbar.search_requested.connect(self.search_requested)
        self.view.searchbar.text_changed.connect(self.text_cleared)
        self.view.searchbar.suggestion_selected.connect(self.suggestion_selected)
        self.view.tableview.row_selected.connect(self.open_details)

    def adv_search_requested(self):
        self.adv_search_dialog = OrderSearchController(self.is_dark,self.model)
        self.adv_search_dialog.view.show()

    def insert_requested(self):
        self.insert_dialog = OrderInsertController(self.is_dark,self.model)
        self.insert_dialog.view.show()
        self.insert_dialog.refresh_requested.connect(self.refresh)

    def remove_requested(self):
        self.remove_dialog = OrderRemoveController(self.is_dark,self.model)
        self.remove_dialog.view.show()
        self.remove_dialog.refresh_requested.connect(self.refresh)

    def refresh(self):
        self.table_data = self.model.fetch_all_data()
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

    def open_details(self, data):
        self.details_dialog = OrderDtlPageController(self.is_dark,data[6],data[5])
        self.details_dialog.view.show()