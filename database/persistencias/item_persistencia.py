from app.models.item import Item
from database.persistencias.persistencia_base import PersistenciaBase


class ItemPersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Item, 'itens')
