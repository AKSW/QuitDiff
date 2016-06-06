from abc import ABCMeta
from QuitDiffSerializer import QuitDiffSerializer

class EccrevDiff(metaclass=ABCMeta):
    def serialize(self, add, delete):
        return "ecc patch"

EccrevDiff.register(QuitDiffSerializer)
