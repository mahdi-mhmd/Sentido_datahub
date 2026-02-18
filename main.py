"""
Application entry point.
Initializes the Qt application and starts the main controller.
"""

import sys
from PySide6.QtWidgets import QApplication

from Controller.MainController import MainController


def main() -> int:
    app = QApplication(sys.argv)

    controller = MainController()
    controller.view.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())