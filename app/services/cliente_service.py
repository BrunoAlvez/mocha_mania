import random

from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.models.cliente import Cliente
from app.models.fidelidade import Fidelidade
from app.models.pedido import Pedido
from app.models.produto import Produto
from app.services.item_service import ItemService
from app.services.service_base import ServiceBase


class ClienteService(ServiceBase):
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
    def pedir(produto: Produto, cliente: Cliente, sem_ingredientes: bool = False) -> Pedido:
        item_service = ItemService()
        if produto.preparado() and not sem_ingredientes:
            for preparo in produto.preparos:
                ingrediente = item_service.encontrar(preparo.ingrediente.id)
                if ingrediente.quantidade < preparo.quantidade:
                    return ClienteService.pedir(produto, cliente, True)
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
            'cliente': cliente,
        }
        fidelidade = cliente.fidelidade
        if fidelidade is not None:
            fidelidade.pontos += random.randint(1, 10)
            fidelidade.update()
            cliente.fidelidade = fidelidade
            cliente.update()
        return Pedido(**dados).create()

    @staticmethod
    def fidelizar(cliente: Cliente) -> Fidelidade:
        cliente.fidelidade = Fidelidade().create()
        cliente.update()
        return cliente.fidelidade

    @staticmethod
    def validar_usuario(login: str, senha: str) -> Cliente or None:
        for cliente in Cliente.all():
            if (cliente.email == login or cliente.login == login) and cliente.senha == senha:
                return cliente
        return None
