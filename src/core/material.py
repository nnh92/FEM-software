class Material:
    """
    Chứa thông tin vật liệu
    Ví dụ: bê tông, thép, thép dự ứng lực...
    """
    def __init__(self, material_id: int, name: str, E: float, nu: float, density: float):
        self.id = material_id
        self.name = name
        self.E = E            # modulus of elasticity [Pa]
        self.nu = nu          # Poisson ratio
        self.density = density  # [kg/m3]
        # có thể thêm fc, fy, gamma… tùy vật liệu