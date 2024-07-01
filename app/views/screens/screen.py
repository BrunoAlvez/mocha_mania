from abc import ABC, abstractmethod

import PySimpleGUI as sg


class Screen(ABC):
    def __iter__(self):
        return iter(self._layout())

    @abstractmethod
    def _layout(self) -> list:
        pass

    def tratar_componentes(self, window: sg.Window, key: str):
        pass

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        pass
