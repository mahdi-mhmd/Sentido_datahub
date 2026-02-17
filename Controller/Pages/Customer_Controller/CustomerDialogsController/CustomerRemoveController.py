from PySide6.QtCore import QObject,Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.Customer_Page.Customer_Dialogs.CustomerRemoveDialog import CustomerRemoveDialog


class CustomerRemoveController(QObject):
    refresh_requested = Signal()

    def __init__(self, theme,model):
        super(CustomerRemoveController, self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.setup_view()
        self.setup_signals()

        self.error = None

    def setup_view(self):
        names = self.model.fetch_distinct_values("Name")
        self.view = CustomerRemoveDialog(self.is_dark, names)

    def setup_signals(self):
        self.view.remove_requested.connect(self.remove_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.name_changed.connect(self.add_comboboxes_items)

    def remove_requested(self):
        customer_name = self.none_if_empty(self.view.customer_name.currentText())
        customer_tel = self.none_if_empty(self.view.customer_tel.currentText())
        customer_city = self.none_if_empty(self.view.customer_city.currentText())
        customer_address = self.none_if_empty(self.view.customer_address.currentText())

        result,success = self.model.remove(customer_name,customer_tel,customer_city,customer_address)
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

