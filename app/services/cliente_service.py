from app.controllers.estoque_controller import EstoqueController
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.models.cliente import Cliente
from app.models.fidelidade import Fidelidade
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.services.item_service import ItemService
from app.services.pedido_service import PedidoService
from app.services.service_base import ServiceBase
from database.seeders.cliente_seeder import ClienteSeeder


class ClienteService(ServiceBase):
    def __init__(self, item_service: ItemService, pedido_service: PedidoService):
        self.__clientes = ClienteSeeder.run()
        self.__item_service = item_service
        self.__pedido_service = pedido_service

    @property
    def clientes(self) -> [Cliente]:
        return self.__clientes

    def cadastrar(self, dados: dict) -> Cliente:
        erros = []
        for cliente_registrado in self.__clientes:
            if cliente_registrado.email == dados['email']:
                erros.append({'email': 'Email já cadastrado'})
            if cliente_registrado.login == dados['login']:
                erros.append({'login': 'Login já cadastrado'})
            if cliente_registrado.cpf == dados['cpf']:
                erros.append({'cpf': 'CPF já cadastrado'})
            if cliente_registrado.telefone == dados['telefone']:
                erros.append({'telefone': 'Telefone já cadastrado'})
        if len(erros) > 0:
            raise RegraDeNegocioException('Email, login, CPF ou telefone já cadastrado', {
                'erros': erros,
            })
        cliente = Cliente(**dados)
        self.__clientes.append(cliente)
        return cliente

    def atualizar(self, cliente: Cliente, dados: dict) -> Cliente:
        for atributo, valor in dados.items():
            setattr(cliente, atributo, valor)
        return cliente

    def remover(self, id: int):
        cliente_removido = self.encontrar(id)
        self.__clientes.remove(cliente_removido)

    def encontrar(self, id: int) -> Cliente or None:
        for cliente in self.__clientes:
            if cliente.id == id:
                return cliente
        raise Exception('Cliente não encontrado')

    def listar(self, filtros: dict = None) -> [Cliente]:
        return self.__clientes

    def cadastrar_fidelidade(self, id: int) -> Fidelidade:
        cliente_com_fidelidade = self.encontrar(id)
        cliente_com_fidelidade.fidelidade = Fidelidade()
        return cliente_com_fidelidade.fidelidade

    def pedir(self, produto: Produto, cliente: Cliente) -> Pedido:
        if produto.preparado():
            for preparo in produto.preparos:
                ingrediente = self.__item_service.encontrar(preparo.ingrediente.id)
                if ingrediente.quantidade < preparo.quantidade:
                    raise RegraDeNegocioException('Ingrediente insuficiente')
                else:
                    self.__item_service.retirar(ingrediente, preparo.quantidade)
        else:
            if produto.quantidade < 1:
                raise RegraDeNegocioException('Produto indisponível')
            self.__item_service.retirar(produto, 1)
        dados = {
            'id': self.__pedido_service.get_id(self.__pedido_service.pedidos),
            'itens': [produto],
            'cliente': cliente
        }
        self.__pedido_service.cadastrar(dados)
        return self.__pedido_service.encontrar(dados['id'])

    def validar_usuario(self, login: str, senha: str) -> Cliente or None:
        for cliente in self.__clientes:
            if (cliente.email == login or cliente.login == login) and cliente.senha == senha:
                return cliente
        return None
