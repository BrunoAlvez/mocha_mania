from copy import copy

from app.enums.unidade_enum import UnidadeEnum
from app.helpers.input import input_int
from app.views.view_base import ViewBase


class EstoqueView(ViewBase):
    @staticmethod
    def menu() -> int:
        print('###         Estoque         ###')
        print('Escolha uma opção:')
        return input_int(
            '[1] Listar - [2] Cadastrar - [0] Voltar\n'
        )

    @staticmethod
    def listar(itens: list):
        if len(itens) == 0:
            print('Digite "0" (zero) para sair')
            print('Nenhum item cadastrado\n')
        else:
            print(' | '.join(['      ID      ', '     Nome     ', '     Tipo    ']))
            for item in itens:
                print(' | '.join([str(item['id']), item['nome'], item['tipo']]))
            print('Digite "0" (zero) para sair')
            print('Digite o ID do item para mais opções\n')
        return input_int()

    def cadastro(self, tipo: int, dados_anteriores={}, erros={}) -> tuple[dict, int]:
        print('###         Cadastro         ###')
        print('Digite "0" (zero) para sair')
        if len(dados_anteriores) > 0:
            print('Os seguintes campos estão incorretos:')
        else:
            tipo = self.__input_int_tipo_item('Tipo: * ')
            print('Digite as informações a seguir.')
            print('Campos obrigatórios serão marcados com asterístico (*).')

        campos_errados = [list(erro.keys())[0] for erro in erros]
        mensagens_de_erro = {list(erro.keys())[0]: list(erro.values())[0] for erro in erros}
        dados = copy(dados_anteriores)
        if 'nome' not in dados_anteriores:
            if 'nome' in campos_errados:
                print(mensagens_de_erro['nome'])
            dados['nome'] = self._input_str_com_sair('Nome: * ')
        if 'quantidade' not in dados_anteriores:
            if 'quantidade' in campos_errados:
                print(mensagens_de_erro['quantidade'])
            dados['quantidade'] = self._input_str_com_sair('Quantidade: * ')
        if 'unidade' not in dados_anteriores and tipo != 1:
            if 'unidade' in campos_errados:
                print(mensagens_de_erro['unidade'])
            print('Unidades de medida:')
            contador = 1
            unidades = []
            for unidade in UnidadeEnum:
                print(f'[{contador}] - {unidade.descricao()}')
                unidades.append({'unidade': unidade})
                contador += 1
            unidade_id = self._input_int_com_sair('Unidade: * ', 1, contador)
            dados['unidade'] = unidades[unidade_id - 1]['unidade']
        if tipo == 1:
            if 'descricao' not in dados_anteriores:
                if 'descricao' in campos_errados:
                    print(mensagens_de_erro['descricao'])
                dados['descricao'] = self._input_str_com_sair('Descrição: * ')
            if 'preco' not in dados_anteriores:
                if 'preco' in campos_errados:
                    print(mensagens_de_erro['preco'])
                dados['preco'] = self._input_str_com_sair('Preço: * ')
        return dados, tipo

    @staticmethod
    def sucesso_ao_cadastrar(item: dict):
        print(f"Item #{item['id']} cadastrado com sucesso!")

    @staticmethod
    def detalhes(item: dict) -> int:
        print('###         Detalhes         ###')
        print(f'ID: {item["id"]}')
        print(f'Nome: {item["nome"]}')
        print(f'Quantidade: {item["quantidade"]} ({item["unidade"].descricao()})')
        return input_int('[1] Atualizar - [2] Reabastecer - [3] Remover - [0] Sair\n', 0, 3)

    def atualizacao(self, tipo: int, dados_anteriores={}, erros={}) -> dict:
        print('###         Atualização         ###')
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
        if tipo == 1:
            if 'descricao' not in dados_anteriores:
                if 'descricao' in campos_errados:
                    print(mensagens_de_erro['descricao'])
                dados['descricao'] = self._input_str_com_sair('Descrição: * ')
            if 'preco' not in dados_anteriores:
                if 'preco' in campos_errados:
                    print(mensagens_de_erro['preco'])
                dados['preco'] = self._input_str_com_sair('Preço: * ')
        return dados

    @staticmethod
    def sucesso_ao_atualizar(item: dict):
        print(f"Item #{item['id']} atualizado com sucesso!")

    @staticmethod
    def reabastecimento(item: dict) -> float:
        print('###         Reabastecimento         ###')
        print(f'ID: {item["id"]}')
        print(f'Nome: {item["nome"]}')
        print(f'Quantidade: {item["quantidade"]} ({item["unidade"].descricao()})')
        return input_int('Digite a quantidade a ser reabastecida: ')

    @staticmethod
    def sucesso_ao_reabastecer(funcionario: dict):
        print(f"Item #{funcionario['id']} reabastecido com sucesso!")

    @staticmethod
    def remocao() -> int:
        return input_int('Tem certeza que deseja remover o item?\n[1] - Sim [2] - Não\n')

    @staticmethod
    def sucesso_ao_remover(funcionario: dict):
        print(f"Item #{funcionario['id']} removido com sucesso!")

    def __input_int_tipo_item(self, mensagem: str) -> int:
        print('Tipos de item:')
        print('[1] Produto - [2] Ingrediente')
        try:
            tipo = self._input_int_com_sair(mensagem)
            if tipo not in [1, 2]:
                raise ValueError
            return tipo
        except ValueError:
            print('Digite um valor válido')
            return self.__input_int_tipo_item(mensagem)

    @staticmethod
    def estoque_vazio():
        print('O estoque está vazio!')
