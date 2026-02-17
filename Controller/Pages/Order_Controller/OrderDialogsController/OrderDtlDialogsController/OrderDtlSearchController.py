from View.Pages.Order_Page.Order_Dialogs.OrderDtl_Dialogs.OrderDtlSearchDialog import OrderDtlSearchDialog


class OrderDtlSearchController:

    def __init__(self,theme,model,order_id):

        self.is_dark = theme
        self.model = model
        self.view = None
        self.headers = ["Type","Name","Color","Serial","Unit price","Count"]
        self.edit_dialog = None
        self.order_id = order_id

        self.setup_view()
        self.setup_signals()

    def setup_view(self):
        types = self.model.fetch_distinct_values("Type")
        self.view = OrderDtlSearchDialog(self.is_dark, types,self.headers, None)

    def setup_signals(self):
        self.view.adv_search_requested.connect(self.adv_search_requested)
        self.view.close_requested.connect(self.view.close)
        self.view.type_changed.connect(self.add_comboboxes_items)

    def adv_search_requested(self):
        product_type = self.none_if_empty(self.view.product_type.currentText())
        product_name = self.none_if_empty(self.view.product_name.currentText())
        product_color = self.none_if_empty(self.view.product_color.currentText())

        result = self.model.adv_search(self.order_id,product_type,product_name,product_color)
        self.view.tableview.update_data(result)

    def add_comboboxes_items(self, product_type: str):
        names,colors = self.model.fetch_comboboxes_items(product_type)
        self.view.add_comboboxes_items(names,colors)

    @staticmethod
    def none_if_empty(text):
        if type(text) == str:
            text = text.strip()
        return None if text == "" else text

