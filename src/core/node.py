class Node:
    def __init__(self, node_id: int, x: float, y: float, z: float):
        self.id = node_id
        self.x = x
        self.y = y
        self.z = z
        self.bc = [0, 0, 0, 0, 0, 0]  # [Ux, Uy, Uz, Rx, Ry, Rz], 0 = free, 1 = fixed