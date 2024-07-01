from datetime import datetime

from app.controllers.controller_base import ControllerBase
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.models.cliente import Cliente
from app.services.cliente_service import ClienteService
from app.services.item_service import ItemService
from app.services.pedido_service import PedidoService


class ClienteController(ControllerBase):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado = ClienteService.encontrar(usuario_logado_id)

    @property
    def usuario_logado(self) -> Cliente:
        return self.__usuario_logado

    def pedir(self, produto_id: int):
        try:
            produto = ItemService.encontrar_produto(produto_id)
            ClienteService.pedir(produto, self.usuario_logado)
            print(PedidoService.listar({'cliente_id': self.usuario_logado.id}))
            return True
        except RegraDeNegocioException as e:
            return False

    def historico(self, data: str = None):
        filtros = {}
        if self.__usuario_logado is not None:
            filtros['cliente_id'] = self.__usuario_logado.id
        if data is not None:
            data = datetime.strptime(data, '%d/%m/%Y')
            filtros['data'] = data

        pedidos = PedidoService.listar(filtros)
        pedidos_repositorio = []
        for pedido in pedidos:
            pedidos_repositorio.append(self._repositorio(pedido))
        return pedidos_repositorio

    def perfil(self):
        return self._repositorio(Cliente.find(self.__usuario_logado.id))

    def atualizar(self, dados: dict):
        erros = []
        if 'confirmacao_senha' in dados:
            erros = [{'confirmacao_senha': 'A senha e a confirmação de senha não coincidem.'}]
        try:
            return self._repositorio(ClienteService.atualizar(self.__usuario_logado, dados))
        except RegraDeNegocioException as e:
            erros_validacao = e.dados_extras['erros']
            for atributo, erro in [(erro, erros_validacao[0][erro]) for erro in erros_validacao[0]]:
                erros.append({atributo: erro})
            return {
                'erros': erros,
            }

    def remover(self):
        ClienteService.remover(self.__usuario_logado.id)

    @staticmethod
    def validar_usuario(login: str, senha: str) -> Cliente or None:
        return ClienteService.validar_usuario(login, senha)
