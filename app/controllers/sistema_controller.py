from copy import copy

from app.controllers.controller_base import ControllerBase
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.exceptions.throttle_exception import ThrottleException
from app.models.cliente import Cliente
from app.models.pessoa import Pessoa
from app.services.cliente_service import ClienteService
from app.services.funcionario_service import FuncionarioService


class SistemaController(ControllerBase):
    def login_cliente(self, dados: dict, throttle: int = 0):
        try:
            login = dados['login']
            senha = dados['senha']
            usuario = ClienteService.validar_usuario(login, senha)
            return self.__validacoes_login(usuario, throttle)
        except ThrottleException as _:
            self._sair()

    def login_funcionario(self, dados: dict, throttle: int = 0):
        try:
            login = dados['login']
            senha = dados['senha']
            usuario = FuncionarioService.validar_usuario(login, senha)
            return self.__validacoes_login(usuario, throttle)
        except ThrottleException as _:
            self._sair()

    @staticmethod
    def __validacoes_login(usuario: Pessoa or None, throttle: int = 0):
        if usuario is None:
            if throttle == 3:
                raise ThrottleException('Número máximo de tentativas excedido')
            return {
                'throttle': throttle + 1,
                'erros': [
                    'Não conseguimos encontrar um usuário com essas credenciais. Tente novamente.',
                ],
            }
        else:
            return {'usuario.id': usuario.id}

    def cadastrar(self, dados: dict = None):
        if dados is None:
            dados = {}
        erros = []
        try:
            if dados['confirmacao_senha'] != dados['senha']:
                erros = [{'confirmacao_senha': 'As senhas não conferem'}]
            dados_validos = copy(dados)
            dados_validos.pop('confirmacao_senha')
            cliente = Cliente(**dados_validos)
            if erros:
                raise RegraDeNegocioException('Erros de validação', dados_extras={'erros': erros})
            cliente.create()
            self.login_cliente({'login': cliente.login, 'senha': dados['senha']})
        except RegraDeNegocioException as e:
            erros_validacao = e.dados_extras.get('erros')
            erros_validacao.reverse()
            for erro_atributo in erros_validacao:
                for atributo, erro in erro_atributo.items():
                    erros.append({atributo: erro})
            return {
                'erros': erros,
            }
        except ThrottleException as _:
            self._sair()
