from app.models.ingrediente import Ingrediente
from database.persistencias.persistencia_base import PersistenciaBase


class IngredientePersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Ingrediente, 'itens')
