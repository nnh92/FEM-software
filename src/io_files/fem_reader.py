# io/rmbridge_reader.py
from core.project import Project
from core.node import Node
from core.element import Element

def load_rm(path: str, project: Project):
    project.nodes.clear()
    project.elements.clear()

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("NODE"):
                parts = line.split()
                node_id = int(parts[1])
                x, y, z = map(float, parts[2:5])
                project.nodes.append(Node(node_id, x, y, z))
            elif line.startswith("ELEMENT"):
                parts = line.split()
                elem_id = int(parts[1])
                n1, n2 = map(int, parts[2:4])
                mat_id, sec_id = map(int, parts[4:6])
                project.elements.append(Element(elem_id, [n1, n2], mat_id, sec_id))
    project.filename = path