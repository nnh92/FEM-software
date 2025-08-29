# src/core/section.py
from analysis.section_properties import SectionProperties, compute_polygon_properties


class Section:
    def __init__(self, sec_id, name, points, material=None):
        self.id = sec_id
        self.name = name
        self.points = points
        self.material = material

        # Tự động tính properties
        self.properties = SectionProperties(points)

    @property
    def A(self): return self.properties.A
    @property
    def Ix(self): return self.properties.Ix
    @property
    def Iy(self): return self.properties.Iy
    @property
    def Ixy(self): return self.properties.Ixy
    @property
    def J(self): return self.properties.J
    @property
    def cx(self): return self.properties.cx
    @property
    def cy(self): return self.properties.cy
