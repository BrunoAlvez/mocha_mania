from app.enums.unidade_enum import UnidadeEnum
from app.models.item import Item


class Ingrediente(Item):
    def __init__(self, nome: str, quantidade: float, unidade: UnidadeEnum):
        super().__init__(nome, quantidade, unidade)

    @staticmethod
    def persistencia():
        from database.persistencias.ingrediente_persistencia import IngredientePersistencia
        return IngredientePersistencia()

    @staticmethod
    def all() -> list:
        return [item for item in Ingrediente.persistencia().buscar() if isinstance(item, Ingrediente)]

    @staticmethod
    def find(id: int) -> 'Ingrediente':
        return Ingrediente.persistencia().visualizar(id)
