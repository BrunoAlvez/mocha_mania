from abc import ABC, abstractmethod

from app.models.model_base import ModelBase


class ControllerBase(ABC):
    @abstractmethod
    def __init__(self, view):
        self._view = view

    @abstractmethod
    def menu(self):
        pass

    @staticmethod
    def _repositorio(modelo: ModelBase) -> dict:
        return modelo.to_dict()

    def _sair(self, ao_sair: callable = None, forcar: bool = False):
        if forcar:
            exit()
        opcao = self._view.sair()
        if opcao == 1:
            if ao_sair is not None:
                ao_sair()
            else:
                exit()
        else:
            self.menu()
