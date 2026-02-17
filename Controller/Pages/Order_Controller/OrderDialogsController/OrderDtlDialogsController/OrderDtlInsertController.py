from PySide6.QtCore import QObject, Signal

from View.MainElements.MessageDialog import MessageDialog
from View.Pages.Order_Page.Order_Dialogs.OrderDtl_Dialogs.OrderDtlInsertDialog import OrderDtlInsertDialog


class OrderDtlInsertController(QObject):
    refresh_requested = Signal()

    def __init__(self,theme,model,order_id):
        super(OrderDtlInsertController,self).__init__()
        self.message = None
        self.is_dark = theme
        self.model = model
        self.view = None
        self.order_id = order_id
        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = OrderDtlInsertDialog(self.is_dark, types)

    def setup_signals(self):
        self.view.insert_requested.connect(self.insert_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def insert_requested(self):
        product_type = self.none_if_empty(self.view.product_type.currentText())
        product_name = self.none_if_empty(self.view.product_name.currentText())
        product_color = self.none_if_empty(self.view.product_color.currentText())
        serial = self.none_if_empty(self.view.serial_serial.text())
        product_count = self.view.p_count.value()

        result,success = self.model.insert(self.order_id,product_type,product_name,product_color,serial,product_count)
        self.message = MessageDialog(self.is_dark, result,success)
        self.message.show()

        self.refresh_requested.emit()

    def add_comboboxes_items(self, product_type: str):
        names, colors = self.model.fetch_comboboxes_items(product_type)
        self.view.add_comboboxes_items(names,colors)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

