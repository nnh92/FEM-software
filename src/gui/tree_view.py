# src/gui/tree_view.py
from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QModelIndex

class ModelTreeView(QTreeView):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.main_window = None  # sẽ set sau
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Model Tree'])
        self.root_node = self.model.invisibleRootItem()

        self.setModel(self.model)
        self.expandAll()

    def add_menu_tree(self, tree_actions):
        """
        tree_actions: dict, ví dụ
        {
            "Properties": ["Material", "Section"],
            "Structure": ["Node", "Element"],
            "Schedule": ["Load Combinations", "Load Set", "Load Case", "Load Train", "Lane"],
            "Results": ["Displacement", "Moment", "Shear", "Axial", "Reactions"]
        }
        """
        for parent_name, children in tree_actions.items():
            parent_item = QStandardItem(parent_name)
            parent_item.setData("parent", Qt.ItemDataRole.UserRole)
            parent_item.setEditable(False)  # KHÔNG cho rename
            for child_name in children:
                child_item = QStandardItem(child_name)
                child_item.setData("child", Qt.ItemDataRole.UserRole)
                child_item.setEditable(False)  # KHÔNG cho rename
                parent_item.appendRow(child_item)
            self.root_node.appendRow(parent_item)
        self.expandAll()

    def mouseDoubleClickEvent(self, event):
        index = self.indexAt(event.position().toPoint())
        if not index.isValid():
            super().mouseDoubleClickEvent(event)
            return
        item = self.model.itemFromIndex(index)
        item_type = item.data(Qt.ItemDataRole.UserRole)
        if item_type == "parent":
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
        elif item_type == "child" and self.main_window:
            self.main_window.handle_tree_action(item.text())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self.main_window:
            self.main_window.result_display.show_3d()
        else:
            super().keyPressEvent(event)

    def set_main_window(self, main_win):
        self.main_window = main_win