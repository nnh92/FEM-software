# main.py
import sys
from PyQt6.QtWidgets import QApplication
from MainWindowRM import MainWindowRM

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindowRM()

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = App()
    app.run()