from app.models.produto import Produto
from database.persistencias.persistencia_base import PersistenciaBase


class ProdutoPersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Produto, 'itens')
