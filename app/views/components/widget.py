from abc import ABC, abstractmethod


class Widget(ABC):
    def __iter__(self):
        return iter(self.builder())

    @abstractmethod
    def builder(self) -> list:
        pass
