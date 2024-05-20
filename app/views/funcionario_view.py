from copy import copy

from app.enums.cargo_enum import CargoEnum
from app.helpers.input import input_int
from app.views.view_base import ViewBase


class FuncionarioView(ViewBase):
    @staticmethod
    def menu() -> int:
        print('###         Menu         ###')
        print('Escolha um módulo:')
        return input_int(
            '[1] Funcionários - [2] Estoque - [3] Receitas - [4] Pedidos - [0] Sair\n',
            0,
            4,
        )

    @staticmethod
    def menu_funcionarios(acesso_gerente: bool) -> int:
        print('###         Funcionários         ###')
        print('Escolha uma opção:')
        if acesso_gerente:
            return input_int(
                '[1] Listar - [2] Cadastrar - [0] Sair\n'
            )
        return input_int(
            'Escolha uma opção:\n'
            '[1] Listar - [0] Sair\n'
        )

    @staticmethod
    def listar(funcionarios: list):
        if len(funcionarios) == 0:
            print('Digite "0" (zero) para sair')
            print('Nenhum funcionário cadastrado\n')
        else:
            print(' | '.join(['      ID      ', '     Nome     ', '     Email    ']))
            for funcionario in funcionarios:
                print(' | '.join([str(funcionario['id']), funcionario['nome'], funcionario['email']]))
            print('Digite "0" (zero) para sair')
            print('Digite o ID do funcionário para mais opções\n')
        return input_int()

    def cadastro(self, dados_anteriores={}, erros={}) -> dict:
        print('###         Cadastro         ###')
        print('Digite "0" (zero) para sair')
        if len(dados_anteriores) > 0:
            print('Os seguintes campos estão incorretos:')
        else:
            print('Digite as informações a seguir.')
            print('Campos obrigatórios serão marcados com asterístico (*).')

        campos_errados = [list(erro.keys())[0] for erro in erros]
        mensagens_de_erro = {list(erro.keys())[0]: list(erro.values())[0] for erro in erros}
        dados = copy(dados_anteriores)
        if 'nome' not in dados_anteriores:
            if 'nome' in campos_errados:
                print(mensagens_de_erro['nome'])
            dados['nome'] = self._input_str_com_sair('Nome: * ')
        if 'login' not in dados_anteriores:
            if 'login' in campos_errados:
                print(mensagens_de_erro['login'])
            dados['login'] = self._input_str_com_sair('Login: * ')
        if 'email' not in dados_anteriores:
            if 'email' in campos_errados:
                print(mensagens_de_erro['email'])
            dados['email'] = self._input_str_com_sair('E-mail: * ')
        if 'senha' not in dados_anteriores:
            if 'senha' in campos_errados:
                print(mensagens_de_erro['senha'])
            dados['senha'] = self._input_str_com_sair('Senha: * ')
            dados['confirmacao_senha'] = self._input_str_com_sair('Confirmação de senha: * ')
        if 'cargo' not in dados_anteriores:
            if 'cargo' in campos_errados:
                print(mensagens_de_erro['cargo'])
            print('Cargos disponíveis:')
            contador = 1
            cargos = []
            for cargo in CargoEnum:
                if cargo.value == CargoEnum.GERENTE.value:
                    continue
                print(f'[{contador}] - {cargo.descricao()}')
                cargos.append({'cargo': cargo})
                contador += 1
            cargo_id = self._input_int_com_sair('Cargo: * ', 1, contador)
            dados['cargo'] = cargos[cargo_id - 1]['cargo']
        return dados

    @staticmethod
    def sucesso_ao_cadastrar(funcionario: dict):
        print(f"Funcionário #{funcionario['id']} cadastrado com sucesso!")

    @staticmethod
    def detalhes(funcionario: dict, apenas_visualizacao: bool) -> int:
        if isinstance(funcionario['cargo'], int):
            cargo = CargoEnum.cargo_por_id(funcionario['cargo']).descricao()
        else:
            cargo = funcionario['cargo'].descricao()

        print('###         Detalhes         ###')
        print(f'ID: {funcionario["id"]}')
        print(f'Nome: {funcionario["nome"]}')
        print(f'Email: {funcionario["email"]}')
        print(f'Cargo: {cargo}')
        if apenas_visualizacao:
            return input_int('[0] - Sair\n')
        if funcionario['cargo'] == CargoEnum.GERENTE:
            return input_int('[1] - Atualizar - [0] - Sair\n', 0, 1)
        return input_int('[1] - Atualizar - [2] - Remover - [0] - Sair\n', 0, 2)

    def atualizacao(self,
                    funcionario: dict,
                    acesso_gerente: bool,
                    dados_anteriores={},
                    erros={},
                    ) -> dict:
        print('###         Atualizar         ###')
        print('Digite "0" (zero) para sair')
        if len(dados_anteriores) > 0:
            print('Os seguintes campos estão incorretos:')
        else:
            print('Digite as informações a seguir.')
            print('Campos obrigatórios serão marcados com asterístico (*).')

        campos_errados = [list(erro.keys())[0] for erro in erros]
        mensagens_de_erro = {list(erro.keys())[0]: list(erro.values())[0] for erro in erros}
        dados = copy(dados_anteriores)
        if 'nome' not in dados_anteriores:
            if 'nome' in campos_errados:
                print(mensagens_de_erro['nome'])
            dados['nome'] = self._input_str_com_sair('Nome: * ')
        if 'login' not in dados_anteriores:
            if 'login' in campos_errados:
                print(mensagens_de_erro['login'])
            dados['login'] = self._input_str_com_sair('Login: * ')
        if 'senha' not in dados_anteriores:
            if 'senha' in campos_errados:
                print(mensagens_de_erro['senha'])
            dados['senha'] = self._input_str_com_sair('Senha: * ')
            dados['confirmacao_senha'] = self._input_str_com_sair('Confirmação de senha: * ')
        if 'cargo' not in dados_anteriores and acesso_gerente and funcionario['cargo'] != CargoEnum.GERENTE:
            if 'cargo' in campos_errados:
                print(mensagens_de_erro['cargo'])
            print('Cargos disponíveis:')
            contador = 1
            cargos = []
            for cargo in CargoEnum:
                if cargo.value == CargoEnum.GERENTE.value:
                    continue
                print(f'[{contador}] - {cargo.descricao()}')
                cargos.append({'cargo': cargo})
                contador += 1
            cargo_id = self._input_int_com_sair('Cargo: * ', 1, contador)
            dados['cargo'] = cargos[cargo_id - 1]['cargo']
        return dados

    @staticmethod
    def sucesso_ao_atualizar(funcionario: dict):
        print(f"Funcionário #{funcionario['id']} atualizado com sucesso!")

    @staticmethod
    def remocao() -> int:
        return input_int('Tem certeza que deseja remover o funcionário?\n[1] - Sim [2] - Não\n')

    @staticmethod
    def sucesso_ao_remover(funcionario: dict):
        print(f"Funcionário #{funcionario['id']} removido com sucesso!")
