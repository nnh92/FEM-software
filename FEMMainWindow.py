<<<<<<< HEAD
# FEMMainWindow.py
from PyQt6.QtWidgets import QMainWindow, QApplication, QMenu, QPushButton
from PyQt6.QtGui import QAction
import numpy as np

from FEM_GUI_RM import FEM_GUI
from gui.node_dialog import NodeDialog

class FEMMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StructCal FEM Software")
        self.resize(1200, 800)

        self.fem_gui = FEM_GUI()
        self.setCentralWidget(self.fem_gui)

        self.node_list = []     # danh sách node [ [x,y,z], ... ]
        self.node_fixed = []    # danh sách điều kiện biên [ [fx,fy,fz], ... ]

        # Khi update node/element từ Table:
        self.nodes = np.empty((0,3))
        self.elements = np.empty((0,2), dtype=int)
        self.fem_gui.nodes = self.nodes.copy()
        self.fem_gui.elements = self.elements.copy()
        self.fem_gui.structure_loaded = True  # đánh dấu đã có cấu trúc

        # Viewer 3D
        self.create_menus()
        self.connect_actions()
        self.fem_gui.draw_structure()  # nếu draw_structure được viết lại trong RM GUI

    def create_menus(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        self.new_action = QAction("New", self)
        self.open_action = QAction("Open", self)
        self.save_action = QAction("Save", self)
        self.exit_action = QAction("Exit", self)
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Properties Menu
        prop_menu = menubar.addMenu("Properties")
        self.material_action = QAction("Material", self)
        self.section_action = QAction("Section", self)
        prop_menu.addAction(self.material_action)
        prop_menu.addAction(self.section_action)

        # Structure Menu
        struct_menu = menubar.addMenu("Structure")
        self.node_action = QAction("Node", self)
        self.elem_action = QAction("Element", self)
        struct_menu.addAction(self.node_action)
        struct_menu.addAction(self.elem_action)

        # Schedule Menu
        sched_menu = menubar.addMenu("Schedule")
        self.load_com_action = QAction("Load Combinations", self)
        self.load_set_action = QAction("Load Set", self)
        self.load_case_action = QAction("Load Case", self)
        self.load_Train_action = QAction("Load Train", self)
        self.load_Lane_action = QAction("Lane", self)
        sched_menu.addAction(self.load_com_action)
        sched_menu.addAction(self.load_set_action)
        sched_menu.addAction(self.load_case_action)
        sched_menu.addAction(self.load_Lane_action)

        # Results Menu
        results_menu = menubar.addMenu("Results")
        self.disp_action = QAction("Displacement", self)
        self.moment_action = QAction("Moment", self)
        self.shear_action = QAction("Shear", self)
        self.axial_action = QAction("Axial", self)
        self.reaction_action = QAction("Reactions", self)
        for act in [self.disp_action, self.moment_action, self.shear_action,
                    self.axial_action, self.reaction_action]:
            results_menu.addAction(act)

    def connect_actions(self):
        self.exit_action.triggered.connect(self.close)
        # Bạn có thể connect các action còn lại với các hàm tương ứng
        self.disp_action.triggered.connect(lambda: self.fem_gui.plot_displacement())
        self.moment_action.triggered.connect(lambda: self.fem_gui.plot_moment_gui('Mz'))
        self.node_action.triggered.connect(self.open_node_dialog)

    def open_node_dialog(self):
        dlg = NodeDialog(self.node_list, self.node_fixed)
        if dlg.exec():
            self.node_list = dlg.nodes
            self.node_fixed = dlg.fixed
            # --- Cập nhật 3D view nếu cần ---
            if hasattr(self, 'fem_gui') and self.fem_gui.structure_loaded:
                self.fem_gui.nodes = np.array(self.node_list)
                self.fem_gui.draw_structure()

    def run_fem(self):
        if self.fem_gui.structure_loaded:
            self.fem_gui.run_fem()
=======
# FEMMainWindow.py
from PyQt6.QtWidgets import QMainWindow, QApplication, QMenu, QPushButton
from PyQt6.QtGui import QAction
import numpy as np

from FEM_GUI_RM import FEM_GUI
from gui.node_dialog import NodeDialog

class FEMMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StructCal FEM Software")
        self.resize(1200, 800)

        self.fem_gui = FEM_GUI()
        self.setCentralWidget(self.fem_gui)

        self.node_list = []     # danh sách node [ [x,y,z], ... ]
        self.node_fixed = []    # danh sách điều kiện biên [ [fx,fy,fz], ... ]

        # Khi update node/element từ Table:
        self.nodes = np.empty((0,3))
        self.elements = np.empty((0,2), dtype=int)
        self.fem_gui.nodes = self.nodes.copy()
        self.fem_gui.elements = self.elements.copy()
        self.fem_gui.structure_loaded = True  # đánh dấu đã có cấu trúc

        # Viewer 3D
        self.create_menus()
        self.connect_actions()
        self.fem_gui.draw_structure()  # nếu draw_structure được viết lại trong RM GUI

    def create_menus(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        self.new_action = QAction("New", self)
        self.open_action = QAction("Open", self)
        self.save_action = QAction("Save", self)
        self.exit_action = QAction("Exit", self)
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Properties Menu
        prop_menu = menubar.addMenu("Properties")
        self.material_action = QAction("Material", self)
        self.section_action = QAction("Section", self)
        prop_menu.addAction(self.material_action)
        prop_menu.addAction(self.section_action)

        # Structure Menu
        struct_menu = menubar.addMenu("Structure")
        self.node_action = QAction("Node", self)
        self.elem_action = QAction("Element", self)
        struct_menu.addAction(self.node_action)
        struct_menu.addAction(self.elem_action)

        # Schedule Menu
        sched_menu = menubar.addMenu("Schedule")
        self.load_com_action = QAction("Load Combinations", self)
        self.load_set_action = QAction("Load Set", self)
        self.load_case_action = QAction("Load Case", self)
        self.load_Train_action = QAction("Load Train", self)
        self.load_Lane_action = QAction("Lane", self)
        sched_menu.addAction(self.load_com_action)
        sched_menu.addAction(self.load_set_action)
        sched_menu.addAction(self.load_case_action)
        sched_menu.addAction(self.load_Lane_action)

        # Results Menu
        results_menu = menubar.addMenu("Results")
        self.disp_action = QAction("Displacement", self)
        self.moment_action = QAction("Moment", self)
        self.shear_action = QAction("Shear", self)
        self.axial_action = QAction("Axial", self)
        self.reaction_action = QAction("Reactions", self)
        for act in [self.disp_action, self.moment_action, self.shear_action,
                    self.axial_action, self.reaction_action]:
            results_menu.addAction(act)

    def connect_actions(self):
        self.exit_action.triggered.connect(self.close)
        # Bạn có thể connect các action còn lại với các hàm tương ứng
        self.disp_action.triggered.connect(lambda: self.fem_gui.plot_displacement())
        self.moment_action.triggered.connect(lambda: self.fem_gui.plot_moment_gui('Mz'))
        self.node_action.triggered.connect(self.open_node_dialog)

    def open_node_dialog(self):
        dlg = NodeDialog(self.node_list, self.node_fixed)
        if dlg.exec():
            self.node_list = dlg.nodes
            self.node_fixed = dlg.fixed
            # --- Cập nhật 3D view nếu cần ---
            if hasattr(self, 'fem_gui') and self.fem_gui.structure_loaded:
                self.fem_gui.nodes = np.array(self.node_list)
                self.fem_gui.draw_structure()

    def run_fem(self):
        if self.fem_gui.structure_loaded:
            self.fem_gui.run_fem()
>>>>>>> 202dd40af5f3e594f3d2243f95ccd748a2ac9c16
            print("FEM finished. Results are ready.")