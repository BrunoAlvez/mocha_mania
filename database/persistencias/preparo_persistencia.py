from app.models.preparo import Preparo
from database.persistencias.persistencia_base import PersistenciaBase


class PreparoPersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Preparo)
