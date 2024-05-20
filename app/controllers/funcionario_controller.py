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
    def __init__(self,
                 funcionario_service: FuncionarioService,
                 estoque_controller: EstoqueController,
                 receita_controller: ReceitaController,
                 pedido_controller: PedidoController,
                 item_service: ItemService,
                 pedido_service: PedidoService,
                 ao_sair: callable,
                 ):
        super().__init__(FuncionarioView())
        self.__service = funcionario_service
        self.__estoque_controller = estoque_controller
        self.__receita_controller = receita_controller
        self.__pedido_controller = pedido_controller

        self.__item_service = item_service
        self.__pedido_service = pedido_service

        self.__estoque_controller.ao_sair = self.menu
        self.__receita_controller.ao_sair = self.menu
        self.__pedido_controller.ao_sair = self.menu

        self.__ao_sair = ao_sair

        self.__usuario_logado = None

    @property
    def usuario_logado(self) -> Funcionario:
        return self.__usuario_logado

    @usuario_logado.setter
    def usuario_logado(self, usuario: Funcionario):
        self.__pedido_controller.usuario_logado = usuario
        self.__usuario_logado = usuario

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
            self.__estoque_controller.menu()
        elif opcao == 3:
            if len(self.__item_service.ingredientes()) > 0:
                self.__receita_controller.menu()
            else:
                self.__estoque_controller.estoque_vazio()
                self.menu()
        elif opcao == 4:
            if len(self.__pedido_service.pedidos) > 0:
                self.__pedido_controller.menu()
            else:
                self.__pedido_controller.sem_pedidos()
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
        funcionarios = self.__service.listar()
        funcionarios_repositorio = []
        for funcionario in funcionarios:
            funcionarios_repositorio.append(self._repositorio(funcionario))
        opcao = self._view.listar(funcionarios_repositorio)
        if opcao == 0:
            self.menu_funcionarios()
        else:
            self.__encontrar(opcao)

    def __cadastrar(self, dados_anteriores={}, erros={}):
        try:
            dados = self._view.cadastro(dados_anteriores, erros)
            if dados['confirmacao_senha'] != dados['senha']:
                raise RegraDeNegocioException('As senhas não conferem', {
                    'erros': [
                        {'senha': 'As senhas não conferem'},
                    ],
                })
            dados_validos = copy(dados)
            dados_validos.pop('confirmacao_senha')
            dados_validos['id'] = self.__service.get_id(self.__service.funcionarios)
            funcionario = self.__service.cadastrar(dados_validos)
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

        funcionario = self.__service.encontrar(id)
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

    def __atualizar(self, funcionario: Funcionario, dados_anteriores={}, erros={}):
        acesso_gerente = self.usuario_logado.cargo == CargoEnum.GERENTE

        try:
            dados = self._view.atualizacao(
                self._repositorio(funcionario),
                acesso_gerente,
                dados_anteriores,
                erros,
            )
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
            funcionario_atualizado = self.__service.atualizar(funcionario, dados_validos)
            funcionario_repositorio = self._repositorio(funcionario_atualizado)
            self._view.sucesso_ao_atualizar(funcionario_repositorio)
            self.__encontrar(funcionario_repositorio['id'])
        except RegraDeNegocioException as e:
            erros = e.dados_extras.get('erros')
            atributos_com_erro = [list(erro.keys())[0] for erro in erros]
            dados_anteriores = {chave: valor for chave, valor in dados.items() if chave not in atributos_com_erro}
            self.__atualizar(funcionario=funcionario, dados_anteriores=dados_anteriores, erros=erros)
        except SairException as _:
            self.menu_funcionarios()

    def __remover(self, funcionario: Funcionario):
        acesso_total = self.acesso_total_conta(funcionario.id)
        opcao = self._view.remocao()
        if opcao == 1 and acesso_total:
            self.__service.remover(funcionario.id)
            self._view.sucesso_ao_remover(self._repositorio(funcionario))
            if self.usuario_logado.id == funcionario.id:
                self.__usuario_logado = None
                self.__ao_sair()
            else:
                self.menu_funcionarios()
        else:
            self.__encontrar(funcionario.id)

    def validar_usuario(self, login: str, senha: str) -> Funcionario:
        return self.__service.validar_usuario(login, senha)
