from PySide6.QtCore import QObject,Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.Customer_Page.Customer_Dialogs.CustomerEditDialog import CustomerEditDialog


class CustomerEditController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,row,model):
        super(CustomerEditController,self).__init__()
        self.message = None
        self.is_dark = theme
        self.current_row = row
        self.model = model
        self.view = None

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        names = self.model.fetch_distinct_values("Name")
        self.view = CustomerEditDialog(self.is_dark,names,self.current_row)

        tels, cities,addresses = self.model.fetch_comboboxes_items(self.current_row[0])
        self.view.add_comboboxes_items(tels,cities,addresses)

    def setup_signals(self):
        self.view.edit_requested.connect(self.edit)
        self.view.close_requested.connect(self.view.close)
        self.view.name_changed.connect(self.add_comboboxes_items)

    def add_comboboxes_items(self, customer_name: str):
        tels, cities,addresses = self.model.fetch_comboboxes_items(customer_name)
        self.view.add_comboboxes_items(tels, cities,addresses)

    def edit(self):
        new_data = [self.none_if_empty(self.view.customer_name.currentText()),
                    self.none_if_empty(self.view.customer_tel.currentText()),
                    self.none_if_empty(self.view.customer_city.currentText()),
                    self.none_if_empty(self.view.customer_address.currentText()),
                    self.none_if_empty(self.view.customer_comment.text())]

        result,success = self.model.edit_data(self.current_row,new_data)
        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()
        
        self.refresh_requested.emit()

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text
