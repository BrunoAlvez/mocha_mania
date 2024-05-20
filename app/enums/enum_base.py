from abc import abstractmethod
from enum import Enum


class EnumBase(Enum):
    @abstractmethod
    def descricao(self):
        pass

    @classmethod
    def casos(cls):
        return [(caso.value, caso.name) for caso in cls]

    @classmethod
    def valores(cls):
        return [caso.value for caso in cls]

    @classmethod
    def nomes(cls):
        return [caso.name for caso in cls]

    @classmethod
    def obter_nome(cls, valor):
        for caso in cls:
            if caso.value == valor:
                return caso.name
        return None

    @classmethod
    def obter_valor(cls, nome):
        for caso in cls:
            if caso.name == nome:
                return caso.value
        return None
