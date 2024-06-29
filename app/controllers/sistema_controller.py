from copy import copy

from app.controllers.cliente_controller import ClienteController
from app.controllers.controller_base import ControllerBase
from app.controllers.funcionario_controller import FuncionarioController
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.exceptions.sair_exception import SairException
from app.models.cliente import Cliente
from app.models.pessoa import Pessoa
from app.services.cliente_service import ClienteService
from app.services.funcionario_service import FuncionarioService
from app.views.sistema_view import SistemaView


class SistemaController(ControllerBase):
    def __init__(self):
        super().__init__(SistemaView())

    def menu(self):
        opcao = self._view.menu()
        if opcao == 1:
            self.__login_cliente()
        elif opcao == 2:
            self.cadastrar()
        elif opcao == 0:
            self._sair()
        elif opcao == 7:
            self.__login_funcionario()
        else:
            self.menu()

    def __login_cliente(self, throttle: int = 0):
        try:
            login, senha, throttle = self._view.login(throttle)
            usuario = ClienteService.validar_usuario(login, senha)
            self.__validacoes_login(usuario, throttle, ao_errar=self.__login_cliente)
        except SairException as _:
            self.menu()

    def __login_funcionario(self, throttle: int = 0):
        try:
            login, senha, throttle = self._view.login(throttle)
            usuario = FuncionarioService.validar_usuario(login, senha)
            self.__validacoes_login(usuario, throttle, ao_errar=self.__login_funcionario)
        except SairException as _:
            self.menu()

    def __validacoes_login(self, usuario: Pessoa or None, throttle: int = 0, ao_errar: callable = None):
        if usuario is None:
            if throttle == 3:
                self._view.quantidade_de_tentativas_excedidas()
                self._sair(forcar=True)
            ao_errar(throttle + 1)
        else:
            if isinstance(usuario, Cliente):
                cliente_controller = ClienteController(
                    usuario_logado=usuario,
                    ao_sair=self.menu,
                )
                cliente_controller.menu()
            else:
                funcionario_controller = FuncionarioController(
                    usuario_logado=usuario,
                    ao_sair=self.menu,
                )
                funcionario_controller.menu()

    def cadastrar(self, dados_anteriores: dict = None, erros: dict = None):
        if dados_anteriores is None:
            dados_anteriores = {}
        if erros is None:
            erros = {}

        dados = self._view.cadastro(dados_anteriores, erros)
        try:
            if dados['confirmacao_senha'] != dados['senha']:
                raise RegraDeNegocioException('As senhas não conferem', {
                    'erros': [
                        {'senha': 'As senhas não conferem'},
                    ],
                })
            dados_validos = copy(dados)
            dados_validos.pop('confirmacao_senha')
            cliente = ClienteService.cadastrar(dados_validos)
            cliente_repositorio = self._repositorio(cliente)
            self._view.sucesso_ao_cadastrar(cliente_repositorio)
            self.__login_cliente()
        except RegraDeNegocioException as e:
            erros = e.dados_extras.get('erros')
            atributos_com_erro = [list(erro.keys())[0] for erro in erros]
            dados_anteriores = {chave: valor for chave, valor in dados.items() if chave not in atributos_com_erro}
            self.cadastrar(dados_anteriores=dados_anteriores, erros=erros)
        except SairException as _:
            self.menu()
