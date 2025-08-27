<<<<<<< HEAD
# main_window.py (menu tích hợp)
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QTableWidgetItem
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from .tree_view import ModelTreeView
from .view3d import View3DWidget
from .result_display import ResultDisplay
import numpy as np
from .node_dialog import NodeDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Software")
        self.resize(1400, 900)

        # --- Panel trái: Tree + 3D ---
        self.tree_view = ModelTreeView()
        self.view3d = View3DWidget()
        left_splitter = QSplitter(Qt.Orientation.Vertical)
        left_splitter.addWidget(self.tree_view)
        left_splitter.addWidget(self.view3d)
        left_splitter.setStretchFactor(0, 3)
        left_splitter.setStretchFactor(1, 1)

        # --- Panel phải: Result display (giữ nguyên) ---
        self.result_display = ResultDisplay()

        # --- Split chính trái|phải ---
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(self.result_display)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 4)

        # Layout trung tâm
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(main_splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # --- FEM data placeholder ---
        self.node_list = []
        self.node_fixed = []
        self.nodes = []
        self.elements = []
        self.structure_loaded = False

        # --- Giữ nguyên menu + actions cũ ---
        self.create_menus()
        self.connect_actions()

        # --- Tree view vẫn hoạt động như cũ ---
        self.tree_view.set_main_window(self)
        tree_actions = {
            "Properties": ["Material", "Section"],
            "Structure": ["Node", "Element"],
            "Schedule": ["Load Combinations", "Load Set", "Load Case", "Load Train", "Lane"],
            "Results": ["Displacement", "Moment", "Shear", "Axial", "Reactions"]
        }
        self.tree_view.add_menu_tree(tree_actions)

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

    def show_displacement(self):
        self.result_display.show_results("Displacement results here")

    def show_moment(self):
        self.result_display.show_results("Moment results here")

    def show_shear(self):
        self.result_display.show_results("Shear results here")

    def show_axial(self):
        self.result_display.show_results("Axial results here")

    def show_reactions(self):
        self.result_display.show_results("Reaction results here")

    def connect_actions(self):
        self.node_action.triggered.connect(lambda: self.result_display.show_node_table())
        self.elem_action.triggered.connect(lambda: self.result_display.show_elem_table())
        self.material_action.triggered.connect(lambda: self.result_display.show_material_table())
        self.section_action.triggered.connect(lambda: self.result_display.show_section_table())
        self.load_com_action.triggered.connect(lambda: self.result_display.show_load_comb_table())
        self.load_set_action.triggered.connect(lambda: self.result_display.show_load_set_table())
        self.load_case_action.triggered.connect(lambda: self.result_display.show_load_case_table())
        self.load_Train_action.triggered.connect(lambda: self.result_display.show_load_train_table())
        self.load_Lane_action.triggered.connect(lambda: self.result_display.show_lane_table())
        # Results
        self.disp_action.triggered.connect(lambda: self.result_display.show_results("Displacement results"))
        self.moment_action.triggered.connect(lambda: self.result_display.show_results("Moment results"))
        self.shear_action.triggered.connect(lambda: self.result_display.show_results("Shear results"))
        self.axial_action.triggered.connect(lambda: self.result_display.show_results("Axial results"))
        self.reaction_action.triggered.connect(lambda: self.result_display.show_results("Reaction results"))

    def handle_tree_action(self, name):
        mapping = {
            "Node": lambda: self.result_display.show_node_table(),
            "Element": lambda: self.result_display.show_elem_table(),
            "Material": lambda: self.result_display.show_material_table(),
            "Section": lambda: self.result_display.show_section_table(),
            "Load Combinations": lambda: self.result_display.show_load_comb_table(),
            "Load Set": lambda: self.result_display.show_load_set_table(),
            "Load Case": lambda: self.result_display.show_load_case_table(),
            "Load Train": lambda: self.result_display.show_load_train_table(),
            "Lane": lambda: self.result_display.show_lane_table(),
            "Displacement": lambda: self.result_display.show_results("Displacement results"),
            "Moment": lambda: self.result_display.show_results("Moment results"),
            "Shear": lambda: self.result_display.show_results("Shear results"),
            "Axial": lambda: self.result_display.show_results("Axial results"),
            "Reactions": lambda: self.result_display.show_results("Reaction results"),
        }
        if name in mapping:
=======
# main_window.py (menu tích hợp)
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QTableWidgetItem
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from .tree_view import ModelTreeView
from .view3d import View3DWidget
from .result_display import ResultDisplay
import numpy as np
from .node_dialog import NodeDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Software")
        self.resize(1400, 900)

        # --- Panel trái: Tree + 3D ---
        self.tree_view = ModelTreeView()
        self.view3d = View3DWidget()
        left_splitter = QSplitter(Qt.Orientation.Vertical)
        left_splitter.addWidget(self.tree_view)
        left_splitter.addWidget(self.view3d)
        left_splitter.setStretchFactor(0, 3)
        left_splitter.setStretchFactor(1, 1)

        # --- Panel phải: Result display (giữ nguyên) ---
        self.result_display = ResultDisplay()

        # --- Split chính trái|phải ---
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(self.result_display)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 4)

        # Layout trung tâm
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(main_splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # --- FEM data placeholder ---
        self.node_list = []
        self.node_fixed = []
        self.nodes = []
        self.elements = []
        self.structure_loaded = False

        # --- Giữ nguyên menu + actions cũ ---
        self.create_menus()
        self.connect_actions()

        # --- Tree view vẫn hoạt động như cũ ---
        self.tree_view.set_main_window(self)
        tree_actions = {
            "Properties": ["Material", "Section"],
            "Structure": ["Node", "Element"],
            "Schedule": ["Load Combinations", "Load Set", "Load Case", "Load Train", "Lane"],
            "Results": ["Displacement", "Moment", "Shear", "Axial", "Reactions"]
        }
        self.tree_view.add_menu_tree(tree_actions)

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

    def show_displacement(self):
        self.result_display.show_results("Displacement results here")

    def show_moment(self):
        self.result_display.show_results("Moment results here")

    def show_shear(self):
        self.result_display.show_results("Shear results here")

    def show_axial(self):
        self.result_display.show_results("Axial results here")

    def show_reactions(self):
        self.result_display.show_results("Reaction results here")

    def connect_actions(self):
        # Results
        self.disp_action.triggered.connect(lambda: self.result_display.show_results("Displacement results"))
        self.moment_action.triggered.connect(lambda: self.result_display.show_results("Moment results"))
        self.shear_action.triggered.connect(lambda: self.result_display.show_results("Shear results"))
        self.axial_action.triggered.connect(lambda: self.result_display.show_results("Axial results"))
        self.reaction_action.triggered.connect(lambda: self.result_display.show_results("Reaction results"))

    def handle_tree_action(self, name):
        mapping = {
            "Node": lambda: self.result_display.show_node_table(),
            "Element": lambda: self.result_display.show_elem_table(),
            "Material": lambda: self.result_display.show_material_table(),
            "Section": lambda: self.result_display.show_section_table(),
            "Load Combinations": lambda: self.result_display.show_load_comb_table(),
            "Load Set": lambda: self.result_display.show_load_set_table(),
            "Load Case": lambda: self.result_display.show_load_case_table(),
            "Load Train": lambda: self.result_display.show_load_train_table(),
            "Lane": lambda: self.result_display.show_lane_table(),
            "Displacement": lambda: self.result_display.show_results("Displacement results"),
            "Moment": lambda: self.result_display.show_results("Moment results"),
            "Shear": lambda: self.result_display.show_results("Shear results"),
            "Axial": lambda: self.result_display.show_results("Axial results"),
            "Reactions": lambda: self.result_display.show_results("Reaction results"),
        }
        if name in mapping:
>>>>>>> 202dd40af5f3e594f3d2243f95ccd748a2ac9c16
            mapping[name]()