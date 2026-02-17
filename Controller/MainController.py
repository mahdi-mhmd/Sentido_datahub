from Controller.Pages.EC_Controller.ECPageController import ECPageController
from Controller.Pages.Mech_Controller.MechPageController import MechPageController
from Controller.Pages.PCB_Controller.PCBPageController import PCBPageController
from Controller.Pages.LOM_Controller.LOMPageController import LOMPageController
from Controller.Pages.Product_Controller.ProductPageController import ProductPageController
from Controller.Pages.Customer_Controller.CustomerPageController import CustomerPageController
from Controller.Pages.Serial_Controller.SerialPageController import SerialPageController
from Controller.Pages.Order_Controller.OrderPageController import OrderPageController

from View.MainElements.MainWindow import MainWindow
from Controller.ThemeChecker import is_system_dark_theme

class MainController:
    def __init__(self):
        self.is_dark = is_system_dark_theme()
        self.product_page = ProductPageController(self.is_dark)
        self.ec_page = ECPageController(self.is_dark)
        self.pcb_page = PCBPageController(self.is_dark)
        self.lom_page = LOMPageController(self.is_dark)
        self.customer_page = CustomerPageController(self.is_dark)
        self.serial_page = SerialPageController(self.is_dark)
        self.order_page = OrderPageController(self.is_dark)
        self.mech_page = MechPageController(self.is_dark)

        self.view = MainWindow(self.is_dark,self.product_page.view,self.ec_page.view,self.pcb_page.view,self.lom_page.view,
                               self.customer_page.view,self.serial_page.view,self.order_page.view,self.mech_page.view)

        self.pages = {
        "Component" : self.ec_page.view,
        "PCB" : self.pcb_page.view,
        "LOM" : self.lom_page.view,
        "Product" : self.product_page.view,
        "Customer" : self.customer_page.view,
        "Serial" : self.serial_page.view,
        "Order" : self.order_page.view,
        "Mech" : self.mech_page.view,
        }
        self.setup_signals()

    def setup_signals(self):
        self.view.navbar.page_selected.connect(self.change_page)

    def change_page(self,page: str):
        widget = self.pages.get(page)
        self.view.stack.setCurrentWidget(widget)
