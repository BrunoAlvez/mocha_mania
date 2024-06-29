from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.models.cliente import Cliente
from app.models.fidelidade import Fidelidade
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.services.item_service import ItemService
from app.services.pedido_service import PedidoService
from app.services.service_base import ServiceBase
from database.persistencias.cliente_persistencia import ClientePersistencia


class ClienteService(ServiceBase):
    def __init__(self, item_service: ItemService, pedido_service: PedidoService):
        self.__clientes = ClientePersistencia().buscar()
        self.__item_service = item_service
        self.__pedido_service = pedido_service

    @staticmethod
    def listar(filtros: dict = None) -> [Cliente]:
        return Cliente.all()

    @staticmethod
    def cadastrar(dados: dict) -> Cliente:
        return Cliente(**dados).create()

    @staticmethod
    def atualizar(cliente: Cliente, dados: dict) -> Cliente:
        for atributo, valor in dados.items():
            setattr(cliente, atributo, valor)
        return cliente.update()

    @staticmethod
    def remover(id: int):
        Cliente.delete(Cliente.find(id))

    @staticmethod
    def encontrar(id: int) -> Cliente or None:
        return Cliente.find(id)

    @staticmethod
    def cadastrar_fidelidade(id: int) -> Fidelidade:
        cliente_com_fidelidade = ClienteService.encontrar(id)
        cliente_com_fidelidade.fidelidade = Fidelidade().create()
        return cliente_com_fidelidade.fidelidade

    @staticmethod
    def pedir(produto: Produto, cliente: Cliente, sem_ingredientes: bool = False) -> Pedido:
        item_service = ItemService()
        if produto.preparado() and not sem_ingredientes:
            for preparo in produto.preparos:
                ingrediente = item_service.encontrar(preparo.ingrediente.id)
                if ingrediente.quantidade < preparo.quantidade:
                    return ClienteService.pedir(ingrediente, cliente, True)
                else:
                    item_service.retirar(ingrediente, preparo.quantidade)
        else:
            if produto.quantidade < 1:
                if sem_ingredientes:
                    mensagem = 'Ingredientes e produto indisponíveis'
                else:
                    mensagem = 'Produto indisponível'
                raise RegraDeNegocioException(mensagem)
            item_service.retirar(produto, 1)
        dados = {
            'itens': [produto],
            'cliente': cliente
        }
        return Pedido(**dados).create()

    @staticmethod
    def validar_usuario(login: str, senha: str) -> Cliente or None:
        for cliente in Cliente.all():
            if (cliente.email == login or cliente.login == login) and cliente.senha == senha:
                return cliente
        return None
