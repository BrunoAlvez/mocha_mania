from app.models.cliente import Cliente
from database.persistencias.persistencia_base import PersistenciaBase


class ClientePersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Cliente)
