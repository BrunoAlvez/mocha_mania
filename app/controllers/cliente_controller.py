from datetime import datetime

from app.controllers.controller_base import ControllerBase
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.exceptions.sair_exception import SairException
from app.models.cliente import Cliente
from app.services.cliente_service import ClienteService
from app.services.item_service import ItemService
from app.services.pedido_service import PedidoService
from app.views.cliente_view import ClienteView


class ClienteController(ControllerBase):
    def __init__(self,
                 cliente_service: ClienteService,
                 item_service: ItemService,
                 pedido_service: PedidoService,
                 ao_sair: callable,
                 ):
        super().__init__(ClienteView())
        self.__service = cliente_service
        self.__item_service = item_service
        self.__pedido_service = pedido_service

        self.__ao_sair = ao_sair

        self.__usuario_logado = None

    @property
    def usuario_logado(self) -> Cliente:
        return self.__usuario_logado

    @usuario_logado.setter
    def usuario_logado(self, usuario: Cliente):
        self.__usuario_logado = usuario

    def menu(self):
        opcao = self._view.menu(self.usuario_logado.fidelidade is None)
        if opcao == 1:
            self.__pedir()
        elif opcao == 2:
            self.__historico()
        elif opcao == 3:
            self.__perfil()
        elif opcao == 4 and self.usuario_logado.fidelidade is None:
            self.__fidelizar()
        elif opcao == 0:
            self.__usuario_logado = None
            self._sair(ao_sair=self.__ao_sair)
        else:
            self.menu()

    def __pedir(self):
        produtos_repositorio = []
        for produto in self.__item_service.produtos():
            produtos_repositorio.append(self._repositorio(produto))
        try:
            produto_id = self._view.pedido(produtos_repositorio)
            produto = self.__item_service.encontrar_produto(produto_id)
            pedido = self.__service.pedir(produto, self.usuario_logado)
            self._view.sucesso_ao_pedir(self._repositorio(pedido))
        except RegraDeNegocioException as e:
            self._view.erro_ao_pedir(e.mensagem)
            self.__pedir()
        except SairException:
            pass
        except Exception as e:
            self._view.erro_ao_pedir(e)
            self.__pedir()
        self.menu()

    def __historico(self, data: datetime = None):
        filtros = {}
        if self.__usuario_logado is not None:
            filtros['cliente_id'] = self.__usuario_logado.id
        if data is not None:
            filtros['data'] = data

        pedidos = self.__pedido_service.listar(filtros)

        pedidos_repositorio = []
        for pedido in pedidos:
            pedidos_repositorio.append(self._repositorio(pedido))
        opcao = self._view.historico(pedidos_repositorio)
        if opcao == 0:
            self.menu()
        elif opcao == 1:
            try:
                data_pesquisada = self._view.pesquisa_por_data()
                data_pesquisada = datetime.strptime(data_pesquisada, '%d/%m/%Y')
                self.__historico(data_pesquisada)
            except ValueError:
                self._view.data_invalida()
                self.__historico(data)
        else:
            self.__historico(data)

    def __perfil(self):
        opcao = self._view.perfil(self._repositorio(self.usuario_logado))
        if opcao == 0:
            self.menu()
        else:
            self.__perfil()

    def __fidelizar(self):
        try:
            cliente = self.__service.cadastrar_fidelidade(self.usuario_logado.id)
            self._view.sucesso_ao_fidelizar(cliente)
        except RegraDeNegocioException as e:
            self._view.erro_ao_fidelizar(e)
        self.menu()

    def validar_usuario(self, login: str, senha: str) -> Cliente or None:
        return self.__service.validar_usuario(login, senha)
