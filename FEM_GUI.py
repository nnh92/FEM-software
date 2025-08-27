<<<<<<< HEAD
# FEM_GUI.py
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from Calcrate import Calcrate

class FEM_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Viewer")
        self.resize(1000, 700)

        self.cal = Calcrate()
        self.structure_loaded = False
        self.results_computed = False

        # Layout chính
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Canvas matplotlib
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.canvas.setFocus()
        self.canvas.mpl_connect("scroll_event", self.on_scroll)

        # Toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)

        # Data
        self.nodes = np.empty((0,3))
        self.elements = np.empty((0,2), dtype=int)

    # --- Load structure ---
    def load_structure(self):
        self.cal.データ入力()
        self.nodes = np.array(list(zip(self.cal.節点X, self.cal.節点Y, self.cal.節点Z)))
        self.elements = np.array(self.cal.要素節点) - 1  # 0-based
        self.structure_loaded = True
        self.results_computed = False
        self.draw_structure()

    # --- Run FEM ---
    def run_fem(self):
        try:
            self.cal.データ入力()
            NEQ = self.cal.SkYマトリックス(0)
            self.cal.分布荷重振り分け()
            self.cal.外力add()
            self.cal.decomp(NEQ)
            self.cal.redbak(NEQ)
            self.cal.変位計算()
            self.cal.結果出力()
            self.results_computed = True
            print("FEM finished")
        except Exception as e:
            print("Lỗi khi chạy FEM:", e)

    # --- Chuẩn hóa trục 3D ---
    def prepare_axis(self, title=""):
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')
        ax.set_xlabel("X")
        ax.set_ylabel("Z")  # đứng
        ax.set_zlabel("Y")  # ngang
        ax.set_title(title)
        ax.set_box_aspect([1,1,1])
        ax.view_init(elev=30, azim=-60)
        self.auto_zoom(ax)
        return ax

    # --- Vẽ kết cấu ---
    def draw_structure(self, ax=None):
        created_ax = False
        if ax is None:
            ax = self.prepare_axis("Structure")
            created_ax = True
        for el in self.elements:
            n1, n2, *_ = el
            x = [self.nodes[n1,0], self.nodes[n2,0]]
            y = [self.nodes[n1,2], self.nodes[n2,2]]
            z = [self.nodes[n1,1], self.nodes[n2,1]]
            ax.plot(x, y, z, 'b', lw=2)
        if created_ax:
            self.canvas.draw()

    # --- Scroll zoom ---
    def on_scroll(self, event):
        if not self.fig.axes: return
        ax = self.fig.axes[0]
        base_scale = 1.2
        scale_factor = 1/base_scale if event.button=="up" else base_scale
        xdata, ydata = event.xdata, event.ydata
        if xdata is None or ydata is None: return
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        new_width = (xlim[1]-xlim[0])*scale_factor
        new_height = (ylim[1]-ylim[0])*scale_factor
        relx = (xlim[1]-xdata)/(xlim[1]-xlim[0])
        rely = (ylim[1]-ydata)/(ylim[1]-ylim[0])
        ax.set_xlim([xdata-new_width*(1-relx), xdata+new_width*relx])
        ax.set_ylim([ydata-new_height*(1-rely), ydata+new_height*rely])
        self.canvas.draw()

    # --- Auto Zoom ---
    def auto_zoom(self, ax):
        if len(self.nodes)==0: return
        X, Y, Z = self.nodes[:,0], self.nodes[:,2], self.nodes[:,1]
        ax.set_xlim(np.min(X), np.max(X))
        ax.set_ylim(np.min(Y), np.max(Y))
=======
# FEM_GUI.py
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from Calcrate import Calcrate

class FEM_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Viewer")
        self.resize(1000, 700)

        self.cal = Calcrate()
        self.structure_loaded = False
        self.results_computed = False

        # Layout chính
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Canvas matplotlib
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.canvas.setFocus()
        self.canvas.mpl_connect("scroll_event", self.on_scroll)

        # Toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)

        # Data
        self.nodes = np.empty((0,3))
        self.elements = np.empty((0,2), dtype=int)

    # --- Load structure ---
    def load_structure(self):
        self.cal.データ入力()
        self.nodes = np.array(list(zip(self.cal.節点X, self.cal.節点Y, self.cal.節点Z)))
        self.elements = np.array(self.cal.要素節点) - 1  # 0-based
        self.structure_loaded = True
        self.results_computed = False
        self.draw_structure()

    # --- Run FEM ---
    def run_fem(self):
        try:
            self.cal.データ入力()
            NEQ = self.cal.SkYマトリックス(0)
            self.cal.分布荷重振り分け()
            self.cal.外力add()
            self.cal.decomp(NEQ)
            self.cal.redbak(NEQ)
            self.cal.変位計算()
            self.cal.結果出力()
            self.results_computed = True
            print("FEM finished")
        except Exception as e:
            print("Lỗi khi chạy FEM:", e)

    # --- Chuẩn hóa trục 3D ---
    def prepare_axis(self, title=""):
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')
        ax.set_xlabel("X")
        ax.set_ylabel("Z")  # đứng
        ax.set_zlabel("Y")  # ngang
        ax.set_title(title)
        ax.set_box_aspect([1,1,1])
        ax.view_init(elev=30, azim=-60)
        self.auto_zoom(ax)
        return ax

    # --- Vẽ kết cấu ---
    def draw_structure(self, ax=None):
        created_ax = False
        if ax is None:
            ax = self.prepare_axis("Structure")
            created_ax = True
        for el in self.elements:
            n1, n2, *_ = el
            x = [self.nodes[n1,0], self.nodes[n2,0]]
            y = [self.nodes[n1,2], self.nodes[n2,2]]
            z = [self.nodes[n1,1], self.nodes[n2,1]]
            ax.plot(x, y, z, 'b', lw=2)
        if created_ax:
            self.canvas.draw()

    # --- Scroll zoom ---
    def on_scroll(self, event):
        if not self.fig.axes: return
        ax = self.fig.axes[0]
        base_scale = 1.2
        scale_factor = 1/base_scale if event.button=="up" else base_scale
        xdata, ydata = event.xdata, event.ydata
        if xdata is None or ydata is None: return
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        new_width = (xlim[1]-xlim[0])*scale_factor
        new_height = (ylim[1]-ylim[0])*scale_factor
        relx = (xlim[1]-xdata)/(xlim[1]-xlim[0])
        rely = (ylim[1]-ydata)/(ylim[1]-ylim[0])
        ax.set_xlim([xdata-new_width*(1-relx), xdata+new_width*relx])
        ax.set_ylim([ydata-new_height*(1-rely), ydata+new_height*rely])
        self.canvas.draw()

    # --- Auto Zoom ---
    def auto_zoom(self, ax):
        if len(self.nodes)==0: return
        X, Y, Z = self.nodes[:,0], self.nodes[:,2], self.nodes[:,1]
        ax.set_xlim(np.min(X), np.max(X))
        ax.set_ylim(np.min(Y), np.max(Y))
>>>>>>> 202dd40af5f3e594f3d2243f95ccd748a2ac9c16
        ax.set_zlim(np.min(Z), np.max(Z))