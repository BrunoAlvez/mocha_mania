from app.models.funcionario import Funcionario
from database.persistencias.persistencia_base import PersistenciaBase


class FuncionarioPersistencia(PersistenciaBase):
    def __init__(self):
        super().__init__(Funcionario)
