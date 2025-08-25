from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QHBoxLayout, QWidget, QCheckBox)
from PyQt6.QtCore import Qt, QObject, QEvent

class NodeDialog(QDialog):
    def __init__(self, nodes=None, fixed=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Node Editor")
        self.resize(600, 400)

        self.table = QTableWidget()
        self.table.setColumnCount(4)   # Name, X, Y, Z
        self.table.setHorizontalHeaderLabels(["Node Name", "X", "Y", "Z"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
        self.table.installEventFilter(self)  # cài event filter để bắt Enter

        # nếu nodes rỗng thì tạo 1 dòng trống editable
        if not nodes:
            self.table.setRowCount(1)
            for col in range(4):
                item = QTableWidgetItem("")
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(0, col, item)
        else:
            self.load_nodes(nodes)

        # OK / Cancel
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancel")
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        hlayout = QHBoxLayout()
        hlayout.addWidget(btn_ok)
        hlayout.addWidget(btn_cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(hlayout)
        self.setLayout(layout)

    def load_nodes(self, nodes):
        n = len(nodes)
        self.table.setRowCount(max(n,1))
        for i in range(n):
            for col, value in enumerate([str(i+1)] + [str(v) for v in nodes[i]]):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, col, item)
        # nếu nodes rỗng, vẫn giữ 1 dòng trống
        if n == 0:
            for col in range(4):
                item = QTableWidgetItem("")
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(0, col, item)

    # --- Property để đọc nodes ---
    @property
    def nodes(self):
        nodes = []
        for row in range(self.table.rowCount()):
            try:
                name = self.table.item(row, 0).text()
                x = float(self.table.item(row, 1).text())
                y = float(self.table.item(row, 2).text())
                z = float(self.table.item(row, 3).text())
                nodes.append([name, x, y, z])
            except:
                continue
        return nodes

    # --- Event filter để bắt Enter ---
    def eventFilter(self, source: QObject, event: QEvent):
        if source == self.table and event.type() == QEvent.Type.KeyPress:
            # Thêm hàng mới khi Enter ở dòng cuối
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                row = self.table.currentRow()
                if row == self.table.rowCount() - 1:
                    self.table.insertRow(row+1)
                    name_item = QTableWidgetItem(str(row+2))
                    name_item.setFlags(name_item.flags() | Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row+1, 0, name_item)
                    for col in range(1, 4):
                        self.table.setItem(row+1, col, QTableWidgetItem("0.0"))
                    self.table.setCurrentCell(row+1, 1)
            # Xóa hàng bằng Delete
            elif event.key() == Qt.Key.Key_Delete:
                row = self.table.currentRow()
                if row >= 0:
                    self.table.removeRow(row)
        return super().eventFilter(source, event)