from app.models.receita import Receita
from database.persistencias.persistencia_base import PersistenciaBase


class ReceitaPersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Receita)
