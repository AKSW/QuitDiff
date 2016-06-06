from abc import ABCMeta
from QuitDiffSerializer import QuitDiffSerializer

class EccpatchDiff(metaclass=ABCMeta):
    def serialize(self, add, delete):
        return "ecc patch"

EccpatchDiff.register(QuitDiffSerializer)
