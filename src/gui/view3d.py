# src/gui/result_display.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class View3DWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Label header
        label = QLabel("Result Display")
        label.setStyleSheet("font-weight: bold;")
        layout.addWidget(label)

        # Text area hiển thị kết quả FEM
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setText("Results will appear here.")
        layout.addWidget(self.text_area)

        self.setLayout(layout)
