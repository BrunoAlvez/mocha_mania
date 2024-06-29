from app.models.fidelidade import Fidelidade
from database.persistencias.persistencia_base import PersistenciaBase


class FidelidadePersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Fidelidade)
