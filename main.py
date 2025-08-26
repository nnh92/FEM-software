# main.py
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QStyleFactory
from src.gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))   # ép giao diện sang Fusion
    window = MainWindow()
    window.showMaximized()
    #window.show()
    sys.exit(app.exec())  # <-- exec_()

if __name__ == "__main__":
    main()
