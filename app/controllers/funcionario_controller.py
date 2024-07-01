from app.controllers.controller_base import ControllerBase
from app.models.funcionario import Funcionario
from app.services.funcionario_service import FuncionarioService


class FuncionarioController(ControllerBase):
    def __init__(self, usuario_logado: Funcionario):
        self.__usuario_logado = usuario_logado

    @property
    def usuario_logado(self) -> Funcionario:
        return self.__usuario_logado

    @staticmethod
    def validar_usuario(login: str, senha: str) -> Funcionario:
        return FuncionarioService.validar_usuario(login, senha)
