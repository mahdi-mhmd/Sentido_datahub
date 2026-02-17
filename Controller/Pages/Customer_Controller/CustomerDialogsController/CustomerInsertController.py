from PySide6.QtCore import QObject, Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.Customer_Page.Customer_Dialogs.CustomerInsertDialog import CustomerInsertDialog


class CustomerInsertController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,model):
        super(CustomerInsertController,self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        names = self.model.fetch_distinct_values("Name")
        self.view = CustomerInsertDialog(self.is_dark, names)

    def setup_signals(self):
        self.view.insert_requested.connect(self.insert_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.name_changed.connect(self.add_comboboxes_items)

    def insert_requested(self):
        customer_name = self.none_if_empty(self.view.customer_name.currentText())
        customer_tel = self.none_if_empty(self.view.customer_tel.currentText())
        customer_city = self.none_if_empty(self.view.customer_city.currentText())
        customer_address = self.none_if_empty(self.view.customer_address.currentText())
        customer_comment = self.none_if_empty(self.view.customer_comment.text())

        if customer_name is None or customer_tel is None or customer_city is None or customer_address is None:
            self.message = MessageDialog(self.is_dark, "Please fill the required fields", 0)
            self.message.show()
            return

        result,success = self.model.insert(customer_name,customer_tel,customer_city,customer_address,customer_comment)
        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()

        self.refresh_requested.emit()

    def add_comboboxes_items(self, customer_name: str):
        tels, cities,addresses = self.model.fetch_comboboxes_items(customer_name)
        self.view.add_comboboxes_items(tels,cities,addresses)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

