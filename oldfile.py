import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from Calcrate import Calcrate
from FEMUtils import FEMUtils

class FEM_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEM Viewer")
        self.resize(1000, 700)

        self.cal = Calcrate()
        self.structure_loaded = False
        self.results_computed = False

        # Layout chính
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Canvas matplotlib
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas)
        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.canvas.setFocus()
        self.canvas.mpl_connect("scroll_event", self.on_scroll)

        # Toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.toolbar)

        # Nút
        btn_layout = QHBoxLayout()
        main_layout.addLayout(btn_layout)

        self.btn_load = QPushButton("Load Structure")
        self.btn_run = QPushButton("Run FEM")
        self.btn_moment = QPushButton("Vẽ Moment")
        self.btn_disp = QPushButton("Vẽ Chuyển vị")
        self.btn_shear = QPushButton("Vẽ Lực cắt")
        self.btn_axial = QPushButton("Vẽ Lực dọc")
        self.btn_reactions = QPushButton("Vẽ Phản lực")
        self.btn_fit = QPushButton("Fit View")

        for btn in [self.btn_load, self.btn_run, self.btn_moment, self.btn_disp,
                    self.btn_shear, self.btn_axial, self.btn_reactions, self.btn_fit]:
            btn_layout.addWidget(btn)

        # Kết nối nút
        self.btn_load.clicked.connect(self.load_structure)
        self.btn_run.clicked.connect(self.run_fem)
        self.btn_disp.clicked.connect(self.plot_displacement)
        self.btn_moment.clicked.connect(lambda: self.plot_moment_gui('Mz'))
        self.btn_shear.clicked.connect(lambda: self.plot_shear_gui('Qy'))
        self.btn_axial.clicked.connect(self.plot_axial_gui)
        self.btn_reactions.clicked.connect(self.plot_reactions_gui)
        self.btn_fit.clicked.connect(self.fit_view)

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
            import traceback; traceback.print_exc()

    # --- Chuẩn hóa trục 3D ---
    def prepare_axis(self, title=""):
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')
        ax.set_xlabel("X (Longitudinal)")
        ax.set_ylabel("Z (Lateral)")
        ax.set_zlabel("Y (Vertical)")
        ax.set_title(title)
        ax.set_box_aspect([1,1,1])
        ax.view_init(elev=30, azim=-60)  # góc nhìn mặc định
        self.auto_zoom(ax)
        return ax

    # --- Vẽ kết cấu ---
    def draw_structure(self, ax=None):
        created_ax = False
        if ax is None:
            ax = self.prepare_axis("Structure")
            created_ax = True

        for el in self.elements:
            n1, n2 = el
            x = [self.nodes[n1][0], self.nodes[n2][0]]
            y = [self.nodes[n1][2], self.nodes[n2][2]]  # đứng
            z = [self.nodes[n1][1], self.nodes[n2][1]]  # ngang
            ax.plot(x, y, z, 'b', lw=2)

        if created_ax:
            self.canvas.draw()

    # --- Vẽ chuyển vị ---
    def plot_displacement(self, scale=10.0):
        if not self.results_computed:
            print("Chưa tính FEM")
            return
        ax = self.prepare_axis("Displacement")
        self.draw_structure(ax)
        for el in self.elements:
            n1, n2 = el
            x = [self.nodes[n1][0] + scale*self.cal.変位[n1][0],
                 self.nodes[n2][0] + scale*self.cal.変位[n2][0]]
            y = [self.nodes[n1][2] + scale*self.cal.変位[n1][2],
                 self.nodes[n2][2] + scale*self.cal.変位[n2][2]]
            z = [self.nodes[n1][1] + scale*self.cal.変位[n1][1],
                 self.nodes[n2][1] + scale*self.cal.変位[n2][1]]
            ax.plot(x, y, z, 'g', lw=2)
            # Nhãn node displacement
            xm, ym, zm = np.mean(x), np.mean(y), np.mean(z)
            disp_val = (self.cal.変位[n1] + self.cal.変位[n2])/2
            ax.text(xm, ym, zm, f"({disp_val[0]:.2f},{disp_val[1]:.2f},{disp_val[2]:.2f})", color='g')
        self.auto_zoom(ax, include_forces=True, scale_disp=10.0, scale_force=0.01)
        self.canvas.draw()

    # --- Vẽ Moment ---
    def plot_moment_gui(self, component='Mz'):
        if not self.results_computed:
            print("Chưa tính FEM")
            return

        self.cal.prepare_element_for_gui()  # tính nội lực GUI
        comp_map = {'Mx': self.cal.Mx, 'My': self.cal.My, 'Mz': self.cal.Mz}
        if component not in comp_map:
            print(f"Component {component} không hợp lệ")
            return
        arr = comp_map[component]  # shape = (n_elements, 2)

        ax = self.prepare_axis(f"Moment ({component})")
        self.draw_structure(ax)
        max_val = np.max(np.abs(arr))
        scale = 0.01/max_val if max_val != 0 else 1.0

        for e, el in enumerate(self.elements):
            n1, n2 = el
            x = [self.nodes[n1][0], self.nodes[n2][0]]
            y = [self.nodes[n1][1] + scale*arr[e,0], 
                self.nodes[n2][1] + scale*arr[e,1]]  # Y: trục đứng
            z = [self.nodes[n1][2], self.nodes[n2][2]]  # Z: trục ngang
            ax.plot(x, y, z, 'r', lw=2)
            ax.text(x[0], y[0], z[0], f"{arr[e,0]:.2f}", color='r')
            ax.text(x[1], y[1], z[1], f"{arr[e,1]:.2f}", color='r')
        self.auto_zoom(ax, include_forces=True, scale_disp=10.0, scale_force=0.01)
        self.canvas.draw()

    # --- Vẽ Shear ---
    def plot_shear_gui(self, component='Qy'):
        if not self.results_computed:
            print("Chưa tính FEM")
            return
        self.cal.prepare_element_for_gui()
        comp_map = {'Qy': self.cal.Qy, 'Qz': self.cal.Qz}
        if component not in comp_map:
            print(f"Component {component} không hợp lệ")
            return
        arr = comp_map[component]
        ax = self.prepare_axis(f"Shear ({component})")
        max_val = np.max(np.abs(arr))
        scale = 50.0/max_val if max_val != 0 else 1.0
        for e, el in enumerate(self.elements):
            n1, n2 = el
            x = [self.nodes[n1][0], self.nodes[n2][0]]
            y = [self.nodes[n1][2] + scale*arr[e,0], self.nodes[n2][2] + scale*arr[e,1]]
            z = [self.nodes[n1][1], self.nodes[n2][1]]
            ax.plot(x, y, z, 'b', lw=2)
            xm, ym, zm = np.mean(x), np.mean(y), np.mean(z)
            ax.text(xm, ym, zm, f"{(arr[e,0]+arr[e,1])/2:.2f}", color='b')
        self.auto_zoom(ax, include_forces=True, scale_disp=10.0, scale_force=0.01)
        self.canvas.draw()

    # --- Vẽ Axial ---
    def plot_axial_gui(self):
        if not self.results_computed:
            print("Chưa tính FEM")
            return
        self.cal.prepare_element_for_gui()
        arr = self.cal.N
        ax = self.prepare_axis("Axial Force (N)")
        max_val = np.max(np.abs(arr))
        scale = 50.0/max_val if max_val != 0 else 1.0
        for e, el in enumerate(self.elements):
            n1, n2 = el
            x = [self.nodes[n1][0], self.nodes[n2][0]]
            y = [self.nodes[n1][2], self.nodes[n2][2]]
            z = [self.nodes[n1][1] + scale*arr[e,0], self.nodes[n2][1] + scale*arr[e,1]]
            ax.plot(x, y, z, 'g', lw=2)
            xm, ym, zm = np.mean(x), np.mean(y), np.mean(z)
            ax.text(xm, ym, zm, f"{(arr[e,0]+arr[e,1])/2:.2f}", color='g')
        self.auto_zoom(ax, include_forces=True, scale_disp=10.0, scale_force=0.01)
        self.canvas.draw()

    # --- Vẽ phản lực ---
    def plot_reactions_gui(self):
        if not self.results_computed:
            print("Chưa tính FEM")
            return
        ax = self.prepare_axis("Node Reactions")
        fixed_nodes = np.where(self.cal.is_fixed)[0]
        if len(fixed_nodes) == 0:
            print("Không có node cố định")
            return
        max_val = np.max(np.abs(self.cal.FORCE[fixed_nodes*6 : fixed_nodes*6+6]))
        scale = 50.0 / max_val if max_val != 0 else 1.0
        for i in fixed_nodes:
            x, y, z = self.nodes[i]
            fx, fy, fz = self.cal.FORCE[i*6:i*6+3]
            mx, my, mz = self.cal.FORCE[i*6+3:i*6+6]
            ax.quiver(x, y, z, fx*scale, fy*scale, fz*scale, color='r')
            ax.text(x+0.1, y+0.1, z+0.1, f"F=({fx:.1f},{fy:.1f},{fz:.1f})", color='r')
            ax.quiver(x, y, z, mx*scale, my*scale, mz*scale, color='b')
            ax.text(x+0.1, y+0.1, z+0.1, f"M=({mx:.1f},{my:.1f},{mz:.1f})", color='b')
        self.auto_zoom(ax, include_forces=True, scale_disp=10.0, scale_force=0.01)
        self.canvas.draw()

    # --- Scroll zoom ---
    def on_scroll(self, event):
        ax = self.fig.axes[0] if self.fig.axes else None
        if ax is None:
            return
        base_scale = 1.2
        scale_factor = 1/base_scale if event.button=="up" else base_scale
        xdata = event.xdata
        ydata = event.ydata
        if xdata is None or ydata is None: return
        xlim = ax.get_xlim(); ylim = ax.get_ylim()
        new_width = (xlim[1]-xlim[0])*scale_factor
        new_height = (ylim[1]-ylim[0])*scale_factor
        relx = (xlim[1]-xdata)/(xlim[1]-xlim[0])
        rely = (ylim[1]-ydata)/(ylim[1]-ylim[0])
        ax.set_xlim([xdata-new_width*(1-relx), xdata+new_width*relx])
        ax.set_ylim([ydata-new_height*(1-rely), ydata+new_height*rely])
        self.canvas.draw()

    # --- Auto Zoom ---
    def auto_zoom(self, ax, include_forces=True, scale_disp=10.0, scale_force=1.0):
        X = self.nodes[:,0].copy()
        Y = self.nodes[:,2].copy()  # trục đứng
        Z = self.nodes[:,1].copy()  # trục ngang

        # --- Displacement ---
        if hasattr(self.cal, '変位'):
            X = np.hstack([X, X + scale_disp*self.cal.変位[:,0]])
            Y = np.hstack([Y, Y + scale_disp*self.cal.変位[:,2]])
            Z = np.hstack([Z, Z + scale_disp*self.cal.変位[:,1]])

        # --- Nội lực phần tử ---
        if include_forces:
            # Mx, My, Mz
            for e, el in enumerate(self.elements):
                n1, n2 = el
                # Moment: My/Mz theo trục đứng (Y)
                if hasattr(self.cal, 'Mz'):
                    Y = np.hstack([Y, self.nodes[n1,2] + scale_force*self.cal.Mz[e,0],
                                        self.nodes[n2,2] + scale_force*self.cal.Mz[e,1]])
                    Z = np.hstack([Z, self.nodes[n1,1], self.nodes[n2,1]])
                if hasattr(self.cal, 'My'):
                    Y = np.hstack([Y, self.nodes[n1,2] + scale_force*self.cal.My[e,0],
                                        self.nodes[n2,2] + scale_force*self.cal.My[e,1]])
                    Z = np.hstack([Z, self.nodes[n1,1], self.nodes[n2,1]])
                if hasattr(self.cal, 'Mx'):
                    Z = np.hstack([Z, self.nodes[n1,1] + scale_force*self.cal.Mx[e,0],
                                        self.nodes[n2,1] + scale_force*self.cal.Mx[e,1]])
                    Y = np.hstack([Y, self.nodes[n1,2], self.nodes[n2,2]])
                # Shear và axial: Qy, Qz, N
                if hasattr(self.cal, 'Qy'):
                    Y = np.hstack([Y, self.nodes[n1,2] + scale_force*self.cal.Qy[e,0],
                                        self.nodes[n2,2] + scale_force*self.cal.Qy[e,1]])
                if hasattr(self.cal, 'Qz'):
                    Z = np.hstack([Z, self.nodes[n1,1] + scale_force*self.cal.Qz[e,0],
                                        self.nodes[n2,1] + scale_force*self.cal.Qz[e,1]])
                if hasattr(self.cal, 'N'):
                    # axial: dọc theo X (longitudinal)
                    X = np.hstack([X, self.nodes[n1,0] + scale_force*self.cal.N[e,0],
                                        self.nodes[n2,0] + scale_force*self.cal.N[e,1]])

        # --- Phản lực ---
        if include_forces and hasattr(self.cal, 'FORCE') and hasattr(self.cal, 'is_fixed'):
            fixed_nodes = np.where(self.cal.is_fixed)[0]
            for i in fixed_nodes:
                fx, fy, fz = self.cal.FORCE[i*6:i*6+3]
                mx, my, mz = self.cal.FORCE[i*6+3:i*6+6]
                X = np.hstack([X, self.nodes[i,0] + scale_force*fx])
                Y = np.hstack([Y, self.nodes[i,2] + scale_force*fy])
                Z = np.hstack([Z, self.nodes[i,1] + scale_force*fz])
                # M moment
                X = np.hstack([X, self.nodes[i,0] + scale_force*mx])
                Y = np.hstack([Y, self.nodes[i,2] + scale_force*my])
                Z = np.hstack([Z, self.nodes[i,1] + scale_force*mz])

        # --- Set limits ---
        ax.set_xlim(np.min(X), np.max(X))
        ax.set_ylim(np.min(Y), np.max(Y))
        ax.set_zlim(np.min(Z), np.max(Z))

    # --- Fit View ---
    def fit_view(self):
        if not self.fig.axes: return
        ax = self.fig.axes[0]
        self.auto_zoom(ax)
        self.canvas.draw()
