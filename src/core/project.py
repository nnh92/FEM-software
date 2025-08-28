from .node import Node
from .element import Element
from .material import Material
from .section import Section


class Project:
    """
    Chứa toàn bộ dữ liệu mô hình FEM.
    Không chứa logic đọc/ghi file.
    """
    def __init__(self):
        self.filename = None        # đường dẫn file nếu có
        self.nodes = []             # list[Node]
        self.elements = []          # list[Element]
        self.materials = []         # list[Material]
        self.loadcases = []         # list[LoadCase]
        self.sections = []          # list[Section]

    # --- Các hàm thao tác dữ liệu ---
    # --- Node ---
    def add_node(self, node: Node):
        self.nodes.append(node)

    def remove_node(self, node_id: int):
        self.nodes = [n for n in self.nodes if n.id != node_id]

    # --- Element ---
    def add_element(self, element: Element):
        self.elements.append(element)

    def remove_element(self, element_id: int):
        self.elements = [e for e in self.elements if e.id != element_id]

    # --- Material ---
    def add_material(self, material: Material):
        self.materials.append(material)

    def remove_material(self, mat_id):
        self.materials = [m for m in self.materials if m.id != mat_id]

    # --- Section ---
    def add_section(self, sec: Section):
        self.sections.append(sec)

    def remove_section(self, sec_id):
        self.sections = [s for s in self.sections if s.id != sec_id]

    # --- LoadCase ---
    def add_loadcase(self, loadcase):
        self.loadcases.append(loadcase)
    def remove_loadcase(self, lc_id: int):
        self.loadcases = [loadcase for loadcase in self.loadcases if loadcase.id != lc_id]


    # --- Clear toàn bộ project ---
    def clear(self):
        self.nodes.clear()
        self.elements.clear()
        self.materials.clear()
        self.sections.clear()
        self.loadcases.clear()
        self.filename = None