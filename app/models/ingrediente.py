from app.enums.unidade_enum import UnidadeEnum
from app.models.item import Item


class Ingrediente(Item):
    def __init__(self, id: int, nome: str, quantidade: float, unidade: UnidadeEnum):
        super().__init__(id, nome, quantidade, unidade)
