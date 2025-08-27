# src/gui/result_display.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QStackedWidget, QLabel, QPushButton, QApplication
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeySequence

class ResultDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.stack = QStackedWidget(self)
        self.run_button = QPushButton("RUN")
        self.run_button.setMaximumWidth(80)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

        # Tab 0: 3D view
        self.view3d_label = QLabel("3D View of Structure")
        self.view3d_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stack.addWidget(self.view3d_label)

        # Tab 1: Node table
        self.node_table = QTableWidget()
        self.node_table.setColumnCount(4)
        self.node_table.setHorizontalHeaderLabels(["Node ID", "X", "Y", "Z"])
        self.node_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.node_table.setRowCount(1)
        for col in range(4):
            item = QTableWidgetItem("0" if col == 0 else "0.0")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.node_table.setItem(0, col, item)
        self.stack.addWidget(self.node_table)

        # Tab 2: Material
        self.material_table = QTableWidget()
        self.material_table.setColumnCount(6)
        self.material_table.setHorizontalHeaderLabels(["ID", "Name", "Modulus of Elastic", "Poisson's Ratio", "Thermal Coefficient", "Weight density"])
        self.material_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.material_table.setRowCount(1)
        for col in range(6):
            item = QTableWidgetItem("0" if col == 0 else "0.0")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.material_table.setItem(0, col, item)
        self.stack.addWidget(self.material_table)

        # Tab 3: Section
        self.section_table = QTableWidget()
        self.section_table.setColumnCount(8)
        self.section_table.setHorizontalHeaderLabels(["ID", "Name", "Area", "Ixx", "Iyy", "Izz", "y", "z"])
        self.section_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.section_table.setRowCount(1)
        for col in range(8):
            item = QTableWidgetItem("0" if col == 0 else "0.0")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.section_table.setItem(0, col, item)
        self.stack.addWidget(self.section_table)

        # Tab 4: Element
        self.elem_table = QTableWidget()
        self.elem_table.setColumnCount(6)
        self.elem_table.setHorizontalHeaderLabels(["Element ID", "Node I", "Node J", "Material", "Section I", "Section J"])
        self.elem_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.elem_table.setRowCount(1)
        for col in range(6):
            item = QTableWidgetItem("0" if col == 0 else "0.0")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.elem_table.setItem(0, col, item)
        self.stack.addWidget(self.elem_table)

        # Tab 5~9: Schedule tables
        self.load_comb_table = QTableWidget()
        self.load_comb_table.setColumnCount(3)
        self.load_comb_table.setHorizontalHeaderLabels(["ID", "Name", "Details"])
        self.load_comb_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.load_comb_table.setRowCount(1)
        for col in range(3):
            item = QTableWidgetItem("0" if col == 0 else "0.0")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.load_comb_table.setItem(0, col, item)
        self.stack.addWidget(self.load_comb_table)

        self.load_set_table = QTableWidget()
        self.load_set_table.setColumnCount(3)
        self.load_set_table.setHorizontalHeaderLabels(["ID", "Name", "Details"])
        self.load_set_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.load_set_table.setRowCount(1)
        for col in range(3):
            item = QTableWidgetItem("0" if col == 0 else "0.0")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.load_set_table.setItem(0, col, item)
        self.stack.addWidget(self.load_set_table)

        self.load_case_table = QTableWidget()
        self.load_case_table.setColumnCount(3)
        self.load_case_table.setHorizontalHeaderLabels(["ID", "Name", "Details"])
        self.load_case_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.load_case_table.setRowCount(1)
        for col in range(3):
            item = QTableWidgetItem("0" if col == 0 else "0.0")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.load_case_table.setItem(0, col, item)
        self.stack.addWidget(self.load_case_table)

        self.load_train_table = QTableWidget()
        self.load_train_table.setColumnCount(3)
        self.load_train_table.setHorizontalHeaderLabels(["ID", "Train Type", "Details"])
        self.load_train_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.load_train_table.setRowCount(1)
        for col in range(3):
            item = QTableWidgetItem("0" if col == 0 else "0.0")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.load_train_table.setItem(0, col, item)
        self.stack.addWidget(self.load_train_table)

        self.lane_table = QTableWidget()
        self.lane_table.setColumnCount(3)
        self.lane_table.setHorizontalHeaderLabels(["ID", "Lane Type", "Details"])
        self.lane_table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lane_table.setRowCount(1)
        for col in range(3):
            item = QTableWidgetItem("0" if col == 0 else "0.0")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.lane_table.setItem(0, col, item)
        self.stack.addWidget(self.lane_table)

        # Tab 10: Results
        self.results_label = QTableWidget()
        self.results_label.setColumnCount(3)
        self.results_label.setHorizontalHeaderLabels(["ID", "Results", "Details"])
        self.stack.addWidget(self.results_label)

        # RUN button
        self.run_button.clicked.connect(self.execute_run)

        self._wire_table(self.node_table, editable=True)
        self._wire_table(self.material_table, editable=True)
        self._wire_table(self.section_table, editable=True)
        self._wire_table(self.elem_table, editable=True)
        self._wire_table(self.load_comb_table, editable=True)
        self._wire_table(self.load_set_table, editable=True)
        self._wire_table(self.load_case_table, editable=True)
        self._wire_table(self.load_train_table, editable=True)
        self._wire_table(self.lane_table, editable=True)
        self._wire_table(self.results_label)

    # ----- Show các tab (giữ tên cũ) -----
    def show_3d(self): self.stack.setCurrentWidget(self.view3d_label)
    def show_node_table(self): self.stack.setCurrentWidget(self.node_table); self.node_table.setFocus()
    def show_material_table(self): self.stack.setCurrentWidget(self.material_table); self.material_table.setFocus()
    def show_section_table(self): self.stack.setCurrentWidget(self.section_table); self.section_table.setFocus()
    def show_elem_table(self): self.stack.setCurrentWidget(self.elem_table); self.elem_table.setFocus()
    def show_load_comb_table(self): self.stack.setCurrentWidget(self.load_comb_table); self.load_comb_table.setFocus()
    def show_load_set_table(self): self.stack.setCurrentWidget(self.load_set_table); self.load_set_table.setFocus()
    def show_load_case_table(self): self.stack.setCurrentWidget(self.load_case_table); self.load_case_table.setFocus()
    def show_load_train_table(self): self.stack.setCurrentWidget(self.load_train_table); self.load_train_table.setFocus()
    def show_lane_table(self): self.stack.setCurrentWidget(self.lane_table); self.lane_table.setFocus()
    def show_results(self, text):
        if not hasattr(self, 'results_label'):
            self.results_label = QLabel()
            self.results_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self.results_label.setWordWrap(True)
            self.stack.addWidget(self.results_label)
        self.results_label.setText(text)
        self.stack.setCurrentWidget(self.results_label)
        self.results_label.setFocus()

    # ----- Key event -----
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.show_3d()
        else:
            super().keyPressEvent(event)

    # Tạo các event filter đưa vào __init__
    def _wire_table(self, tbl, editable=False):
        # chọn nhiều ô, copy kiểu Excel
        tbl.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        tbl.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        # chỉ vào edit khi double-click (hoặc để NoEditTriggers nếu chỉ muốn copy)
        tbl.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked if editable
            else QTableWidget.EditTrigger.NoEditTriggers
        )
        tbl.installEventFilter(self)

    # ----- RUN button -----
    def execute_run(self):
        print("RUN button clicked - FEM executing...")

    # ----- Event filter -----
    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:
            # Enter: thêm dòng cho node_table
            if isinstance(source, QTableWidget) and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                row = source.currentRow()
                col = source.currentColumn()
                if row == source.rowCount() - 1:
                    source.insertRow(row+1)
                    id_item = QTableWidgetItem(str(row+2))
                    id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
                    source.setItem(row+1,0,id_item)
                    for col in range(1,4):
                        item = QTableWidgetItem("0.0")
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                        source.setItem(row+1,col,item)
                    source.setCurrentCell(row+1,1)
                else:
                    # Không phải dòng cuối -> xuống dòng tiếp theo, cùng cột
                    source.setCurrentCell(row + 1, col)
                return True
            # Delete: xóa dòng
            elif isinstance(source, QTableWidget) and event.key() == Qt.Key.Key_Delete:
                row = source.currentRow()
                total_rows = source.rowCount()
                if total_rows > 1:
                    source.removeRow(row)
                else:
                    # Nếu chỉ còn 1 dòng -> clear dữ liệu (giữ ID cột 0)
                    item = source.item(row, 0)
                    item.setText("1")
                    for col in range(1, source.columnCount()):
                        item = source.item(row, col)
                        if item:
                            item.setText("0.0")

            # Ctrl+C: copy multi-cell
            elif event.matches(QKeySequence.StandardKey.Copy):
                if isinstance(source, QTableWidget):
                    self.copy_selection_to_clipboard(source)
                return True
            # Ctrl+A
            elif event.matches(QKeySequence.StandardKey.SelectAll):
                if isinstance(source, QTableWidget):
                    source.selectAll()
                    return True
            # Ctrl+V: paste
            elif event.matches(QKeySequence.StandardKey.Paste):
                if isinstance(source, QTableWidget):
                    self.paste_from_clipboard(source)
                return True

            # --- Sự kiện ấn số: tự edit cell ---
            elif isinstance(source, QTableWidget) and Qt.Key.Key_0 <= event.key() <= Qt.Key.Key_9:
                row = source.currentRow()
                col = source.currentColumn()
                item = source.item(row, col)
                if not item:
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                    source.setItem(row, col, item)
                # Bật chế độ editable
                source.editItem(item)
                # Gán luôn giá trị phím vào ô
                key_value = str(event.key() - Qt.Key.Key_0)
                item.setText(key_value)
                return True  # đánh dấu đã xử lý

        return super().eventFilter(source, event)

    # ----- Copy multi-cell -----
    def copy_selection_to_clipboard(self, table: QTableWidget):
        selection = table.selectedRanges()
        if not selection:
            return
        text = ""
        for sel in selection:
            for row in range(sel.topRow(), sel.bottomRow() + 1):
                row_data = []
                for col in range(sel.leftColumn(), sel.rightColumn() + 1):
                    item = table.item(row, col)
                    # Nếu ô chưa có QTableWidgetItem thì tạo
                    if item is None:
                        item = QTableWidgetItem("")
                        table.setItem(row, col, item)
                    row_data.append(item.text())
                text += "\t".join(row_data) + "\n"
        QApplication.clipboard().setText(text)

    # ----- Hàm Paste từ excel sang phần mềm -----
    def paste_from_clipboard(self, table: QTableWidget):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if not text:
            return

        start_row = table.currentRow()
        start_col = table.currentColumn()
        if start_row < 0: start_row = 0
        if start_col < 0: start_col = 0

        rows = text.splitlines()
        for i, row_text in enumerate(rows):
            columns = row_text.split("\t")
            row_idx = start_row + i

            # Nếu vượt số dòng hiện tại, thêm dòng mới
            while row_idx >= table.rowCount():
                table.insertRow(table.rowCount())
                # Tạo item trống có flag editable cho từng cột
                for col in range(table.columnCount()):
                    item = QTableWidgetItem("")
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    table.setItem(table.rowCount() - 1, col, item)

            for j, col_text in enumerate(columns):
                col_idx = start_col + j
                if col_idx >= table.columnCount():
                    break
                item = table.item(row_idx, col_idx)
                if not item:
                    item = QTableWidgetItem()
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    table.setItem(row_idx, col_idx, item)
                item.setText(col_text)

    # ----- Cập nhật node table -----
    def update_node_table(self, node_list):
        self.node_table.setRowCount(len(node_list))
        for i,node in enumerate(node_list):
            id_item = QTableWidgetItem(str(node[0]))
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.node_table.setItem(i,0,id_item)
            for col,val in enumerate(node[1:],start=1):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.node_table.setItem(i,col,item)

    # ----- Cập nhật element table -----
    def update_elelemt_table(self, elelemt_list):
        self.elem_table.setRowCount(len(elelemt_list))
        for i,node in enumerate(elelemt_list):
            id_item = QTableWidgetItem(str(node[0]))
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.elem_table.setItem(i,0,id_item)
            for col,val in enumerate(node[1:],start=1):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.elem_table.setItem(i,col,item)

    # ----- Cập nhật material table -----
    def update_material_table(self, material_list):
        self.material_table.setRowCount(len(material_list))
        for i,node in enumerate(material_list):
            id_item = QTableWidgetItem(str(node[0]))
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.material_table.setItem(i,0,id_item)
            for col,val in enumerate(node[1:],start=1):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.material_table.setItem(i,col,item)

    # ----- Cập nhật section table -----
    def update_section_table(self, section_list):
        self.section_table.setRowCount(len(section_list))
        for i,node in enumerate(section_list):
            id_item = QTableWidgetItem(str(node[0]))
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.section_table.setItem(i,0,id_item)
            for col,val in enumerate(node[1:],start=1):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.section_table.setItem(i,col,item)

    # ----- Cập nhật load com table -----
    def update_loadcom_table(self, loadcom_list):
        self.load_comb_table.setRowCount(len(loadcom_list))
        for i,node in enumerate(loadcom_list):
            id_item = QTableWidgetItem(str(node[0]))
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.load_comb_table.setItem(i,0,id_item)
            for col,val in enumerate(node[1:],start=1):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.load_comb_table.setItem(i,col,item)

    # ----- Cập nhật lc table -----
    def update_loadcase_table(self, loadcase_list):
        self.load_case_table.setRowCount(len(loadcase_list))
        for i,node in enumerate(loadcase_list):
            id_item = QTableWidgetItem(str(node[0]))
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.load_case_table.setItem(i,0,id_item)
            for col,val in enumerate(node[1:],start=1):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.load_case_table.setItem(i,col,item)

    # ----- Cập nhật ls table -----
    def update_loadset_table(self, loadset_list):
        self.load_set_table.setRowCount(len(loadset_list))
        for i,node in enumerate(loadset_list):
            id_item = QTableWidgetItem(str(node[0]))
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.load_set_table.setItem(i,0,id_item)
            for col,val in enumerate(node[1:],start=1):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.load_set_table.setItem(i,col,item)

    # ----- Cập nhật load train table -----
    def update_loadtrain_table(self, loadtrain_list):
        self.load_train_table.setRowCount(len(loadtrain_list))
        for i,node in enumerate(loadtrain_list):
            id_item = QTableWidgetItem(str(node[0]))
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.load_train_table.setItem(i,0,id_item)
            for col,val in enumerate(node[1:],start=1):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.load_train_table.setItem(i,col,item)

    # ----- Cập nhật lane table -----
    def update_lane_table(self, lane_list):
        self.lane_table.setRowCount(len(lane_list))
        for i,node in enumerate(lane_list):
            id_item = QTableWidgetItem(str(node[0]))
            id_item.setFlags(id_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.lane_table.setItem(i,0,id_item)
            for col,val in enumerate(node[1:],start=1):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.lane_table.setItem(i,col,item)