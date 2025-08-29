import numpy as np

def compute_polygon_properties(points):
    """
    Tính toán đặc trưng hình học của mặt cắt polygon.
    Input: points = [(x1, y1), (x2, y2), ...] (điểm theo chiều kim đồng hồ hoặc ngược)
    Output: dict chứa A, cx, cy, Ix, Iy, Ixy, J
    """
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])
    x1 = np.roll(x, -1)
    y1 = np.roll(y, -1)

    # Diện tích (shoelace)
    A = 0.5 * np.sum(x * y1 - x1 * y)

    # Trọng tâm
    Cx = (1 / (6 * A)) * np.sum((x + x1) * (x * y1 - x1 * y))
    Cy = (1 / (6 * A)) * np.sum((y + y1) * (x * y1 - x1 * y))

    # Momen quán tính
    Ix = (1 / 12) * np.sum((y**2 + y * y1 + y1**2) * (x * y1 - x1 * y))
    Iy = (1 / 12) * np.sum((x**2 + x * x1 + x1**2) * (x * y1 - x1 * y))
    Ixy = (1 / 24) * np.sum(
        (x * y1 + 2 * x * y + 2 * x1 * y1 + x1 * y) * (x * y1 - x1 * y)
    )

    # Quy đổi về trọng tâm
    Ix_c = Ix - A * Cy**2
    Iy_c = Iy - A * Cx**2
    Ixy_c = Ixy - A * Cx * Cy

    return {
        "A": abs(A),
        "cx": Cx,
        "cy": Cy,
        "Ix": Ix_c,
        "Iy": Iy_c,
        "Ixy": Ixy_c,
        "J": Ix_c + Iy_c,  # polar moment
    }


class SectionProperties:
    def __init__(self, points):
        self.points = points
        props = compute_polygon_properties(points)
        self.A = props["A"]
        self.cx = props["cx"]
        self.cy = props["cy"]
        self.Ix = props["Ix"]
        self.Iy = props["Iy"]
        self.Ixy = props["Ixy"]
        self.J = props["J"]
