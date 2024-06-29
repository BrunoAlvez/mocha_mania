from copy import copy

from app.controllers.controller_base import ControllerBase
from app.controllers.estoque_controller import EstoqueController
from app.controllers.pedido_controller import PedidoController
from app.controllers.receita_controller import ReceitaController
from app.enums.cargo_enum import CargoEnum
from app.exceptions.regra_de_negocio_exception import RegraDeNegocioException
from app.exceptions.sair_exception import SairException
from app.models.funcionario import Funcionario
from app.services.funcionario_service import FuncionarioService
from app.services.item_service import ItemService
from app.services.pedido_service import PedidoService
from app.views.funcionario_view import FuncionarioView


class FuncionarioController(ControllerBase):
    def __init__(self, usuario_logado: Funcionario, ao_sair: callable):
        super().__init__(FuncionarioView())

        self.__usuario_logado = usuario_logado
        self.__ao_sair = ao_sair

    @property
    def usuario_logado(self) -> Funcionario:
        return self.__usuario_logado

    def acesso_total_conta(self, id: int) -> bool:
        return (
                self.usuario_logado.id == id
                or self.usuario_logado.cargo == CargoEnum.GERENTE
        )

    def menu(self):
        opcao = self._view.menu()
        if opcao == 1:
            self.menu_funcionarios()
        elif opcao == 2:
            EstoqueController(self.menu).menu()
        elif opcao == 3:
            if len(ItemService.ingredientes()) > 0:
                ReceitaController(self.menu).menu()
            else:
                EstoqueController(self.menu).estoque_vazio()
                self.menu()
        elif opcao == 4:
            if len(PedidoService.pedidos()) > 0:
                PedidoController(self.menu).menu()
            else:
                PedidoController(self.menu).sem_pedidos()
                self.menu()
        elif opcao == 0:
            self.__usuario_logado = None
            self._sair(ao_sair=self.__ao_sair)
        else:
            self.menu()

    def menu_funcionarios(self):
        acesso_gerente = self.usuario_logado.cargo == CargoEnum.GERENTE
        opcao = self._view.menu_funcionarios(acesso_gerente)
        if opcao == 1:
            self.__listar()
        elif opcao == 2 and acesso_gerente:
            self.__cadastrar()
        elif opcao == 0:
            self.menu()
        else:
            self.menu_funcionarios()

    def __listar(self):
        funcionarios = FuncionarioService.listar()
        funcionarios_repositorio = []
        for funcionario in funcionarios:
            funcionarios_repositorio.append(self._repositorio(funcionario))
        opcao = self._view.listar(funcionarios_repositorio)
        if opcao == 0:
            self.menu_funcionarios()
        else:
            self.__encontrar(opcao)

    def __cadastrar(self, dados_anteriores=None, erros=None):
        if dados_anteriores is None:
            dados_anteriores = {}
        if erros is None:
            erros = {}
        dados = self._view.cadastro(dados_anteriores, erros)
        try:
            if dados['confirmacao_senha'] != dados['senha']:
                raise RegraDeNegocioException('As senhas não conferem', {
                    'erros': [
                        {'senha': 'As senhas não conferem'},
                    ],
                })
            dados_validos = copy(dados)
            dados_validos.pop('confirmacao_senha')
            funcionario = FuncionarioService.cadastrar(dados_validos)
            funcionario = self._repositorio(funcionario)
            self._view.sucesso_ao_cadastrar(funcionario)
            self.__encontrar(funcionario['id'])
        except RegraDeNegocioException as e:
            erros = e.dados_extras.get('erros')
            atributos_com_erro = [list(erro.keys())[0] for erro in erros]
            dados_anteriores = {chave: valor for chave, valor in dados.items() if chave not in atributos_com_erro}
            self.__cadastrar(dados_anteriores=dados_anteriores, erros=erros)
        except SairException as _:
            self.menu_funcionarios()

    def __encontrar(self, id: int):
        apenas_visualizacao = not self.acesso_total_conta(id)

        funcionario = FuncionarioService.encontrar(id)
        funcionario_repositorio = self._repositorio(funcionario)
        opcao = self._view.detalhes(funcionario_repositorio, apenas_visualizacao)
        if opcao == 0:
            self.menu_funcionarios()
        elif opcao == 1 and not apenas_visualizacao:
            self.__atualizar(funcionario)
        elif opcao == 2 and not apenas_visualizacao:
            self.__remover(funcionario)
        else:
            self.__encontrar(id)

    def __atualizar(self, funcionario: Funcionario, dados_anteriores=None, erros=None):
        if dados_anteriores is None:
            dados_anteriores = {}
        if erros is None:
            erros = {}
        acesso_gerente = self.usuario_logado.cargo == CargoEnum.GERENTE

        dados = self._view.atualizacao(
            self._repositorio(funcionario),
            acesso_gerente,
            dados_anteriores,
            erros,
        )
        try:
            if 'confirmacao_senha' in dados:
                if dados['confirmacao_senha'] != dados['senha']:
                    raise RegraDeNegocioException('As senhas não conferem', {
                        'erros': [
                            {'senha': 'As senhas não conferem'},
                        ],
                    })
            dados_validos = copy(dados)
            if 'confirmacao_senha' in dados_validos:
                dados_validos.pop('confirmacao_senha')
            funcionario_atualizado = FuncionarioService.atualizar(funcionario, dados_validos)
            funcionario_repositorio = self._repositorio(funcionario_atualizado)
            self._view.sucesso_ao_atualizar(funcionario_repositorio)
            self.__encontrar(funcionario_repositorio['id'])
        except RegraDeNegocioException as e:
            erros = e.dados_extras.get('erros')
            atributos_com_erro = [list(erro.keys())[0] for erro in erros]
            dados_anteriores = {chave: valor for chave, valor in dados.items() if chave not in atributos_com_erro}
            self.__atualizar(funcionario=funcionario, dados_anteriores=dados_anteriores, erros=erros)

    def __remover(self, funcionario: Funcionario):
        acesso_total = self.acesso_total_conta(funcionario.id)
        opcao = self._view.remocao()
        if opcao == 1 and acesso_total:
            FuncionarioService.remover(funcionario.id)
            self._view.sucesso_ao_remover(self._repositorio(funcionario))
            if self.usuario_logado.id == funcionario.id:
                self.__usuario_logado = None
                self.__ao_sair()
            else:
                self.menu_funcionarios()
        else:
            self.__encontrar(funcionario.id)

    @staticmethod
    def validar_usuario(login: str, senha: str) -> Funcionario:
        return FuncionarioService.validar_usuario(login, senha)
