from app.models.ingrediente import Ingrediente
from app.models.item import Item
from app.models.preparo import Preparo
from app.models.produto import Produto
from app.services.service_base import ServiceBase
from database.seeders.itens_seeder import ItensSeeder


class ItemService(ServiceBase):
    def __init__(self):
        self.__itens = ItensSeeder.run()

    @property
    def itens(self) -> [Item]:
        return self.__itens

    def produtos(self) -> [Produto]:
        return [item for item in self.__itens if isinstance(item, Produto)]

    def ingredientes(self) -> [Ingrediente]:
        return [item for item in self.__itens if isinstance(item, Ingrediente)]

    def cadastrar(self, dados: dict) -> Item:
        tipo = dados.pop('tipo')
        if tipo is Produto:
            item = self.__cadastrar_produto(dados)
        else:
            item = self.__cadastrar_ingrediente(dados)
        return item

    def __cadastrar_ingrediente(self, dados: dict) -> Ingrediente:
        ingrediente = Ingrediente(**dados)
        self.adicionar_item(ingrediente)
        return ingrediente

    def __cadastrar_produto(self, dados: dict) -> Produto:
        preparos = []
        if 'preparos' in dados:
            for preparo in dados['preparos']:
                ingrediente = self.encontrar(preparo['ingrediente']['id'])
                preparo['ingrediente'] = ingrediente
                preparo['id'] = len(preparos) + 1
                preparos.append(Preparo(**preparo))
        dados['preparos'] = preparos
        if 'quantidade' not in dados:
            dados['quantidade'] = None
        else:
            dados['quantidade'] = float(dados['quantidade'])
        produto = Produto(**dados)
        self.adicionar_item(produto)
        return produto

    def atualizar(self, item: Item, dados: dict) -> Item:
        for atributo, valor in dados.items():
            setattr(item, atributo, valor)
        return item

    def remover(self, id: int):
        item_removido = self.encontrar(id)
        self.__itens.remove(item_removido)

    def encontrar_produto(self, id: int) -> Produto:
        item = self.encontrar(id)
        if isinstance(item, Produto):
            return item
        raise Exception('Produto não encontrado')

    def encontrar(self, id: int) -> Item or None:
        for item in self.__itens:
            if item.id == id:
                return item
        raise Exception('Item não encontrado')

    def listar(self, filtros: dict = None) -> [Item]:
        itens = self.__itens
        if filtros is not None:
            if 'apenas_produtos' in filtros:
                itens = [item for item in itens if isinstance(item, Produto)]
            if 'apenas_ingredientes' in filtros:
                itens = [item for item in itens if isinstance(item, Ingrediente)]
            if 'apenas_preparados' in filtros:
                itens = list(filter(lambda item: isinstance(item, Produto) and item.preparado(), itens))
        return itens

    @staticmethod
    def reabastecer(item: Item, quantidade: float) -> Item:
        quantidade_no_item = float(item.quantidade)
        quantidade_nova = quantidade_no_item + quantidade
        item.quantidade = quantidade_nova
        return item

    @staticmethod
    def retirar(item: Item, quantidade: float) -> Item:
        quantidade_no_item = float(item.quantidade)
        quantidade_nova = quantidade_no_item - quantidade
        item.quantidade = quantidade_nova
        return item

    def adicionar_item(self, item: Item):
        self.__itens.append(item)

    def remover_item(self, item: Item):
        self.__itens.remove(item)
