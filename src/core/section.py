class Section:
    """
    Chứa thông tin mặt cắt của phần tử
    Ví dụ: tiết diện dầm, cột, hộp, tròn…
    """
    def __init__(self, section_id: int, name: str, type_: str, params: dict):
        self.id = section_id
        self.name = name
        self.type = type_       # ví dụ: "I", "Box", "Circular"
        self.params = params    # dictionary lưu các thông số: b, h, tw, tf, D, t…