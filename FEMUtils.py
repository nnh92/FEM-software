<<<<<<< HEAD
class FEMUtils:
    @staticmethod
    def zero_if_small(x, eps=1e-8):
=======
class FEMUtils:
    @staticmethod
    def zero_if_small(x, eps=1e-8):
>>>>>>> 202dd40af5f3e594f3d2243f95ccd748a2ac9c16
        return 0.0 if abs(x) < eps else x