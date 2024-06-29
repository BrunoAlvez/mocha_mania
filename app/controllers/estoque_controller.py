from copy import copy

from app.controllers.controller_base import ControllerBase
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.exceptions.sair_exception import SairException
from app.models.ingrediente import Ingrediente
from app.models.item import Item
from app.models.produto import Produto
from app.services.item_service import ItemService
from app.views.estoque_view import EstoqueView


class EstoqueController(ControllerBase):
    def __init__(self, ao_sair: callable):
        super().__init__(EstoqueView())
        self.__ao_sair = ao_sair

    def menu(self):
        opcao = self._view.menu()
        if opcao == 1:
            self.__listar()
        elif opcao == 2:
            self.__cadastrar()
        elif opcao == 0:
            self.__ao_sair()
        else:
            self.menu()

    def __listar(self):
        itens = ItemService.listar()
        itens_repositorio = []
        for item in itens:
            itens_repositorio.append(self._repositorio(item))
        opcao = self._view.listar(itens_repositorio)
        if opcao == 0:
            self.menu()
        else:
            self.encontrar(opcao)

    def __cadastrar(self, tipo: int = None, dados_anteriores=None, erros=None):
        if dados_anteriores is None:
            dados_anteriores = {}
        if erros is None:
            erros = {}
        dados, tipo = self._view.cadastro(tipo, dados_anteriores, erros)
        try:
            dados_validos = copy(dados)
            dados_validos['tipo'] = Produto if tipo == 1 else Ingrediente
            item = ItemService.cadastrar(dados_validos)
            item = self._repositorio(item)
            self._view.sucesso_ao_cadastrar(item)
            self.encontrar(item['id'])
        except RegraDeNegocioException as e:
            erros = e.dados_extras.get('erros')
            atributos_com_erro = [list(erro.keys())[0] for erro in erros]
            dados_anteriores = {chave: valor for chave, valor in dados.items() if chave not in atributos_com_erro}
            self.__cadastrar(tipo=tipo, dados_anteriores=dados_anteriores, erros=erros)
        except SairException as _:
            self.menu()

    def encontrar(self, id: int):
        item = ItemService.encontrar(id)
        item_repositorio = self._repositorio(item)
        opcao = self._view.detalhes(item_repositorio)
        if opcao == 0:
            self.menu()
        elif opcao == 1:
            self.__atualizar(item)
        elif opcao == 2:
            self.__reabastecer(item)
        elif opcao == 3:
            self.__remover(item)
        else:
            self.encontrar(id)

    def __atualizar(self, item: Item, dados_anteriores=None, erros=None):
        if dados_anteriores is None:
            dados_anteriores = {}
        if erros is None:
            erros = {}
        dados = self._view.atualizacao(
            1 if isinstance(item, Produto) else 2,
            dados_anteriores,
            erros,
        )
        try:
            dados_validos = copy(dados)
            item_atualizado = ItemService.atualizar(item, dados_validos)
            item_repositorio = self._repositorio(item_atualizado)
            self._view.sucesso_ao_atualizar(item_repositorio)
            self.encontrar(item_repositorio['id'])
        except RegraDeNegocioException as e:
            erros = e.dados_extras.get('erros')
            atributos_com_erro = [list(erro.keys())[0] for erro in erros]
            dados_anteriores = {chave: valor for chave, valor in dados.items() if chave not in atributos_com_erro}
            self.__atualizar(item=item, dados_anteriores=dados_anteriores, erros=erros)
        except SairException as _:
            self.menu()

    def __reabastecer(self, item: Item):
        quantidade = self._view.reabastecimento(self._repositorio(item))
        item_atualizado = ItemService.reabastecer(item, quantidade)
        item_repositorio = self._repositorio(item_atualizado)
        self._view.sucesso_ao_reabastecer(item_repositorio)
        self.encontrar(item_repositorio['id'])

    def __remover(self, item: Item):
        opcao = self._view.remocao()
        if opcao == 1:
            ItemService.remover(item.id)
            self._view.sucesso_ao_remover(self._repositorio(item))
            self.menu()
        elif opcao == 0:
            self.menu()
        else:
            self.encontrar(item.id)

    def _repositorio(self, item: Item):
        dados = super()._repositorio(item)
        dados['tipo'] = 'Produto' if isinstance(item, Produto) else 'Ingrediente'
        return dados

    def estoque_vazio(self):
        self._view.estoque_vazio()
