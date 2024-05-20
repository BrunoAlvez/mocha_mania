from copy import copy

from app.controllers.cliente_controller import ClienteController
from app.controllers.controller_base import ControllerBase
from app.controllers.estoque_controller import EstoqueController
from app.controllers.funcionario_controller import FuncionarioController
from app.controllers.pedido_controller import PedidoController
from app.controllers.receita_controller import ReceitaController
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.exceptions.sair_exception import SairException
from app.models.cliente import Cliente
from app.models.pessoa import Pessoa
from app.services.cliente_service import ClienteService
from app.services.funcionario_service import FuncionarioService
from app.services.item_service import ItemService
from app.services.pedido_service import PedidoService
from app.views.sistema_view import SistemaView


class SistemaController(ControllerBase):
    def __init__(self):
        super().__init__(SistemaView())
        self.__usuario_logado = None

        self.__item_service = ItemService()
        self.__pedido_service = PedidoService(self.__item_service)
        self.__cliente_service = ClienteService(self.__item_service, self.__pedido_service)
        self.__funcionario_service = FuncionarioService(self.__item_service, self.__pedido_service)

        self.__estoque_controller = EstoqueController(self.__item_service)
        self.__receita_controller = ReceitaController(self.__item_service)
        self.__pedido_controller = PedidoController(self.__pedido_service)
        self.__cliente_controller = ClienteController(
            self.__cliente_service,
            self.__item_service,
            self.__pedido_service,
            ao_sair=self.menu,
        )
        self.__funcionario_controller = FuncionarioController(
            self.__funcionario_service,
            self.__estoque_controller,
            self.__receita_controller,
            self.__pedido_controller,
            self.__item_service,
            self.__pedido_service,
            ao_sair=self.menu,
        )

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
            usuario = self.__cliente_controller.validar_usuario(login, senha)
            self.__validacoes_login(usuario, throttle, ao_errar=self.__login_cliente)
        except SairException as _:
            self.menu()

    def __login_funcionario(self, throttle: int = 0):
        try:
            login, senha, throttle = self._view.login(throttle)
            usuario = self.__funcionario_controller.validar_usuario(login, senha)
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
            self.__usuario_logado = usuario
            if isinstance(usuario, Cliente):
                self.__cliente_controller.usuario_logado = usuario
                self.__cliente_controller.menu()
            else:
                self.__funcionario_controller.usuario_logado = usuario
                self.__funcionario_controller.menu()

    def cadastrar(self, dados_anteriores={}, erros={}):
        try:
            dados = self._view.cadastro(dados_anteriores, erros)
            if dados['confirmacao_senha'] != dados['senha']:
                raise RegraDeNegocioException('As senhas não conferem', {
                    'erros': [
                        {'senha': 'As senhas não conferem'},
                    ],
                })
            dados_validos = copy(dados)
            dados_validos.pop('confirmacao_senha')
            dados_validos['id'] = self.__cliente_service.get_id(self.__cliente_service.clientes)
            cliente = self.__cliente_service.cadastrar(dados_validos)
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
