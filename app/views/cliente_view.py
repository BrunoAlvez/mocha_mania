from app.helpers.input import input_int
from app.views.view_base import ViewBase


class ClienteView(ViewBase):
    def __init__(self):
        pass

    @staticmethod
    def menu(tem_fidelidade: bool):
        print('###         Cliente         ###')
        print('Escolha uma opção:')
        if tem_fidelidade:
            return input_int('[1] Pedir - [2] Histórico - [3] Perfil - [0] Sair\n')
        return input_int('[1] Pedir - [2] Histórico - [3] Perfil - [4] Fidelizar - [0] Sair\n')

    def pedido(self, produtos: list):
        if len(produtos) == 0:
            print('Não há produtos disponíveis para pedir.')
            return input_int('[0] Voltar\n')
        print('###         Pedir         ###')
        print('Escolha um produto:')
        for produto in produtos:
            print(f'[{produto["id"]}] - {produto["nome"]} - R${produto["preco"]}')
        return self._input_int_com_sair('Digite o número do produto: ', 1)

    @staticmethod
    def erro_ao_pedir(mensagem: str):
        print(f'Erro ao pedir: {mensagem}')

    @staticmethod
    def sucesso_ao_pedir(pedido: dict):
        print(f'Pedido #{pedido["id"]} realizado com sucesso!')

    @staticmethod
    def historico(pedidos: list):
        print('###         Histórico         ###')
        if len(pedidos) == 0:
            print('Digite "0" (zero) para sair')
            print('Nenhum pedido cadastrado\n')
        else:
            print(' | '.join(['      ID      ', '     Data     ', '     Valor     ']))
            for pedido in pedidos:
                print(f'#{pedido["id"]} - {pedido["data"].strftime("%d/%m/%Y")} - R${pedido["valor"]}')
            print('Digite "0" (zero) para sair')
            print('Digite o "1" (um) para filtrar')
        return input_int(minimo=0, maximo=1)

    @staticmethod
    def pesquisa_por_data():
        return input('Digite a data no formato dd/mm/aaaa: ')

    @staticmethod
    def perfil(cliente: dict):
        print(f'Nome: {cliente["nome"]}')
        print(f'Email: {cliente["email"]}')
        print(f'Telefone: {cliente["telefone"]}')
        if cliente.get('fidelidade'):
            print(f'Fidelidade: {cliente["fidelidade"]}')
        return input_int('[0] Voltar\n')

    @staticmethod
    def sucesso_ao_cadastrar(cliente: dict):
        print(f'Cliente {cliente["nome"]} cadastrado com sucesso!')

    @staticmethod
    def sucesso_ao_fidelizar():
        print('Fidelidade cadastrada com sucesso!')
