from app.models.pessoa import Pessoa
from database.persistencias.persistencia_base import PersistenciaBase


class PessoaPersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Pessoa)
