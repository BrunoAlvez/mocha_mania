from app.models.ingrediente import Ingrediente
from app.models.item import Item
from app.models.preparo import Preparo
from app.models.produto import Produto
from app.services.service_base import ServiceBase


class ItemService(ServiceBase):
    @staticmethod
    def cadastrar(dados: dict) -> Item:
        tipo = dados.pop('tipo')
        if tipo is Produto:
            return ItemService.__cadastrar_produto(dados)
        else:
            return ItemService.__cadastrar_ingrediente(dados)

    @staticmethod
    def __cadastrar_ingrediente(dados: dict) -> Ingrediente:
        return Ingrediente(**dados).create()

    @staticmethod
    def __cadastrar_produto(dados: dict) -> Produto:
        preparos = []
        if 'preparos' in dados:
            for preparo in dados['preparos']:
                ingrediente = ItemService.encontrar(preparo['ingrediente']['id'])
                preparo['ingrediente'] = ingrediente
                preparo['id'] = len(preparos) + 1
                preparos.append(Preparo(**preparo))
        dados['preparos'] = preparos
        if 'quantidade' not in dados:
            dados['quantidade'] = None
        else:
            dados['quantidade'] = float(dados['quantidade'])
        return Produto(**dados).create()

    @staticmethod
    def atualizar(item: Item, dados: dict) -> Item:
        for atributo, valor in dados.items():
            setattr(item, atributo, valor)
        return item.update()

    @staticmethod
    def remover(id: int):
        Item.delete(Item.find(id))

    @staticmethod
    def encontrar_produto(id: int) -> Produto:
        return Produto.find(id)

    @staticmethod
    def encontrar(id: int) -> Item or None:
        return Item.find(id)

    @staticmethod
    def listar(filtros: dict = None) -> [Item]:
        itens = Item.all()
        if filtros is not None:
            if 'apenas_produtos' in filtros:
                itens = [item for item in itens if isinstance(item, Produto)]
            if 'apenas_ingredientes' in filtros:
                itens = [item for item in itens if isinstance(item, Ingrediente)]
            if 'apenas_preparados' in filtros:
                itens = list(filter(lambda item: isinstance(item, Produto) and item.preparado(), itens))
        return itens

    def reabastecer(self, item: Item or int, quantidade: float) -> Item:
        if isinstance(item, int):
            item = self.encontrar(item)
        return self.atualizar(item, {'quantidade': float(item.quantidade) + quantidade})

    def retirar(self, item: Item, quantidade: float) -> Item:
        return self.atualizar(item, {'quantidade': float(item.quantidade) - quantidade})

    def verificar_disponibilidade(self, produto: Produto) -> bool:
        if not isinstance(produto, Produto):
            return False
        if produto.preparado() and produto.quantidade <= 0:
            for preparo in produto.preparos:
                ingrediente = self.encontrar(preparo.ingrediente.id)
                if ingrediente.quantidade < preparo.quantidade:
                    return False
            return True
        return produto.quantidade > 0
