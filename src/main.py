# main.py
import sys, os
sys.path.insert(0, os.path.dirname(__file__))  # thêm src vào path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QStyleFactory
from gui.main_window import MainWindow
from io_files.fem_reader import load_rm
from io_files.fem_writer import save_rm

def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))   # ép giao diện sang Fusion
    window = MainWindow()
    window.showMaximized()
    #window.show()
    sys.exit(app.exec())  # <-- exec_()

if __name__ == "__main__":
    main()