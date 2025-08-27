# MainWindow_RM_Full_v2.py
import sys
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QSplitter, QTreeWidget, QTreeWidgetItem,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QVBoxLayout, QWidget
)
from PyQt6.QtCore import Qt

from FEM_GUI import FEM_GUI  # đã bỏ nút

class MainWindowRM(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StructCal - RM Bridge Full Editor")
        self.resize(1600, 900)

        # --- Central Widget ---
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # --- Splitter chính ---
        splitter_main = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter_main)

        # 3D view bên trái
        self.fem_gui = FEM_GUI()
        splitter_main.addWidget(self.fem_gui)

        # Phải: TreeView (top) + Table (bottom)
        splitter_right = QSplitter(Qt.Orientation.Vertical)
        splitter_main.addWidget(splitter_right)

        # TreeView
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Objects"])
        root = QTreeWidgetItem(["Structure"])
        self.nodes_item = QTreeWidgetItem(["Nodes"])
        self.elems_item = QTreeWidgetItem(["Elements"])
        root.addChild(self.nodes_item)
        root.addChild(self.elems_item)
        self.tree.addTopLevelItem(root)
        self.tree.expandAll()
        splitter_right.addWidget(self.tree)

        # Table
        self.table = QTableWidget()
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.AnyKeyPressed |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )
        splitter_right.addWidget(self.table)

        # --- Dummy Data ---
        self.nodes = np.array([[0,0,0],[5,0,0],[5,5,0]])
        self.elements = np.array([[0,1,1],[1,2,1]])  # 0-based

        self.current_table = "Nodes"
        self.update_table_nodes()
        self.fem_gui.nodes = self.nodes.copy()
        self.fem_gui.elements = self.elements.copy()
        self.fem_gui.draw_structure()

        # --- Connect ---
        self.tree.currentItemChanged.connect(self.on_tree_selection)
        self.table.cellChanged.connect(self.on_cell_changed)

    # ----------------------------
    # Table update functions
    # ----------------------------
    def update_table_nodes(self):
        self.current_table = "Nodes"
        self.table.blockSignals(True)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Node", "X","Y","Z","Fixed"])
        row_count = len(self.nodes) + 1
        self.table.setRowCount(row_count)
        for i, n in enumerate(self.nodes):
            self.table.setItem(i,0,QTableWidgetItem(str(i+1)))
            self.table.setItem(i,1,QTableWidgetItem(str(n[0])))
            self.table.setItem(i,2,QTableWidgetItem(str(n[1])))
            self.table.setItem(i,3,QTableWidgetItem(str(n[2])))
            self.table.setItem(i,4,QTableWidgetItem(""))
        # Hàng trống
        self.table.setItem(row_count-1,0,QTableWidgetItem(str(len(self.nodes)+1)))
        self.table.setItem(row_count-1,1,QTableWidgetItem("0.0"))
        self.table.setItem(row_count-1,2,QTableWidgetItem("0.0"))
        self.table.setItem(row_count-1,3,QTableWidgetItem("0.0"))
        self.table.setItem(row_count-1,4,QTableWidgetItem(""))
        self.table.blockSignals(False)

    def update_table_elements(self):
        self.current_table = "Elements"
        self.table.blockSignals(True)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Element","Node1","Node2","Section"])
        row_count = len(self.elements) + 1
        self.table.setRowCount(row_count)
        for i, el in enumerate(self.elements):
            self.table.setItem(i,0,QTableWidgetItem(str(i+1)))
            self.table.setItem(i,1,QTableWidgetItem(str(el[0]+1)))
            self.table.setItem(i,2,QTableWidgetItem(str(el[1]+1)))
            self.table.setItem(i,3,QTableWidgetItem(str(el[2])))
        # Hàng trống
        self.table.setItem(row_count-1,0,QTableWidgetItem(str(len(self.elements)+1)))
        self.table.setItem(row_count-1,1,QTableWidgetItem(str(1)))
        self.table.setItem(row_count-1,2,QTableWidgetItem(str(1)))
        self.table.setItem(row_count-1,3,QTableWidgetItem(str(1)))
        self.table.blockSignals(False)

    # ----------------------------
    # Tree selection
    # ----------------------------
    def on_tree_selection(self, current, previous):
        if current is None: return
        text = current.text(0)
        if text == "Nodes":
            self.update_table_nodes()
            self.table.setVisible(True)
        elif text == "Elements":
            self.update_table_elements()
            self.table.setVisible(True)
        else:
            self.table.setVisible(False)

    # ----------------------------
    # Table edit → update 3D
    # ----------------------------
    def on_cell_changed(self, row, col):
        if self.current_table=="Nodes":
            # thêm node mới
            if row >= len(self.nodes):
                new_node = [
                    float(self.table.item(row,1).text() or 0),
                    float(self.table.item(row,2).text() or 0),
                    float(self.table.item(row,3).text() or 0)
                ]
                self.nodes = np.vstack([self.nodes,new_node])
                self.update_table_nodes()
            else:
                try:
                    self.nodes[row,0] = float(self.table.item(row,1).text())
                    self.nodes[row,1] = float(self.table.item(row,2).text())
                    self.nodes[row,2] = float(self.table.item(row,3).text())
                except:
                    pass
        elif self.current_table=="Elements":
            if row >= len(self.elements):
                new_el = [
                    int(self.table.item(row,1).text())-1,
                    int(self.table.item(row,2).text())-1,
                    int(self.table.item(row,3).text())
                ]
                self.elements = np.vstack([self.elements,new_el])
                self.update_table_elements()
            else:
                try:
                    self.elements[row,0] = int(self.table.item(row,1).text())-1
                    self.elements[row,1] = int(self.table.item(row,2).text())-1
                    self.elements[row,2] = int(self.table.item(row,3).text())
                except:
                    pass

        # cập nhật FEM_GUI
        self.fem_gui.nodes = self.nodes.copy()
        self.fem_gui.elements = self.elements.copy()
        self.fem_gui.draw_structure()