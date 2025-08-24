# main.py
import sys
from PyQt6.QtWidgets import QApplication
from src.gui import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    #window.show()
    sys.exit(app.exec())  # <-- exec_()

if __name__ == "__main__":
    main()
