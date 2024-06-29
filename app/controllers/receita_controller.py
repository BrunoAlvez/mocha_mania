from copy import copy

from app.controllers.controller_base import ControllerBase
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.exceptions.sair_exception import SairException
from app.models.produto import Produto
from app.services.item_service import ItemService
from app.views.receita_view import ReceitaView


class ReceitaController(ControllerBase):
    def __init__(self, ao_sair: callable):
        super().__init__(ReceitaView())
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
        produtos = ItemService.listar(filtros={'apenas_preparados': True})
        produtos_repositorio = []
        for produto in produtos:
            produtos_repositorio.append(self._repositorio(produto))
        opcao = self._view.listar(produtos_repositorio)
        if opcao == 0:
            self.menu()
        else:
            self.__encontrar(opcao)

    def __cadastrar(self, dados_anteriores=None, erros=None):
        if dados_anteriores is None:
            dados_anteriores = {}
        if erros is None:
            erros = {}
        ingredientes = []
        for ingrediente in ItemService.ingredientes():
            ingredientes.append({
                'id': ingrediente.id,
                'nome': ingrediente.nome,
                'unidade': ingrediente.unidade,
            })
        dados = self._view.cadastro(ingredientes, dados_anteriores, erros)
        try:
            dados_validos = copy(dados)
            dados_validos['id'] = ItemService.get_id(ItemService.itens)
            dados_validos['tipo'] = Produto
            produto = ItemService.cadastrar(dados_validos)
            produto = self._repositorio(produto)
            self._view.sucesso_ao_cadastrar(produto)
            self.__encontrar(produto['id'])
        except RegraDeNegocioException as e:
            erros = e.dados_extras.get('erros')
            atributos_com_erro = [list(erro.keys())[0] for erro in erros]
            dados_anteriores = {chave: valor for chave, valor in dados.items() if chave not in atributos_com_erro}
            self.__cadastrar(dados_anteriores=dados_anteriores, erros=erros)
        except SairException as _:
            self.menu()

    def __encontrar(self, id: int):
        produto = ItemService.encontrar(id)
        produto_repositorio = self._repositorio(produto)
        opcao = self._view.detalhes(produto_repositorio)
        if opcao == 0:
            self.menu()
        elif opcao == 1:
            self.__atualizar(produto)
        elif opcao == 2:
            self.__remover(produto)
        else:
            self.__encontrar(id)

    def __atualizar(self, produto: Produto, dados_anteriores=None, erros=None):
        if dados_anteriores is None:
            dados_anteriores = {}
        if erros is None:
            erros = {}
        dados = self._view.atualizacao(
            self._repositorio(produto),
            dados_anteriores,
            erros,
        )
        try:
            dados_validos = copy(dados)
            produto_atualizado = ItemService.atualizar(produto, dados_validos)
            produto_repositorio = self._repositorio(produto_atualizado)
            self._view.sucesso_ao_atualizar(produto_repositorio)
            self.__encontrar(produto_repositorio['id'])
        except RegraDeNegocioException as e:
            erros = e.dados_extras.get('erros')
            atributos_com_erro = [list(erro.keys())[0] for erro in erros]
            dados_anteriores = {chave: valor for chave, valor in dados.items() if chave not in atributos_com_erro}
            self.__atualizar(produto=produto, dados_anteriores=dados_anteriores, erros=erros)
        except SairException as _:
            self.menu()

    def __remover(self, produto: Produto):
        opcao = self._view.remover()
        if opcao == 1:
            ItemService.remover(produto.id)
            self._view.sucesso_ao_remover(self._repositorio(produto))
            self.menu()
        else:
            self.__encontrar(produto.id)
