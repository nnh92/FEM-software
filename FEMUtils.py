class FEMUtils:
    @staticmethod
    def zero_if_small(x, eps=1e-8):
        return 0.0 if abs(x) < eps else x