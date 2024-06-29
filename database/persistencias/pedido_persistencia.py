from app.models.pedido import Pedido
from database.persistencias.persistencia_base import PersistenciaBase


class PedidoPersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Pedido)
