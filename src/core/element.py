class Element:
    def __init__(self, element_id: int, node_ids: list[int], material_id: int, section_id: int):
        self.id = element_id
        self.node_ids = node_ids
        self.material_id = material_id
        self.section_id = section_id
        