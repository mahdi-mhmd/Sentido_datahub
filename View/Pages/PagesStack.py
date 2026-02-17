from PySide6.QtWidgets import QStackedWidget


class PagesStack(QStackedWidget):
    def __init__(self,*pages):
        super().__init__()

        for page in pages:
            self.addWidget(page)
