# io/rmbridge_writer.py
def save_rm(path: str, project):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Nodes\n")
        for n in project.nodes:
            f.write(f"NODE {n.id} {n.x} {n.y} {n.z}\n")
        f.write("# Elements\n")
        for e in project.elements:
            f.write(f"ELEMENT {e.id} {' '.join(map(str,e.node_ids))} {e.material_id} {e.section_id}\n")