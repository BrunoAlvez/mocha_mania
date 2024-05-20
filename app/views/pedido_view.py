from app.enums.status_pedido_enum import StatusPedidoEnum
from app.helpers.input import input_int
from app.views.view_base import ViewBase


class PedidoView(ViewBase):
    @staticmethod
    def menu() -> int:
        print('###         Pedidos         ###')
        print('Escolha uma opção:')
        return input_int('[1] Listar - [0] Voltar\n')

    @staticmethod
    def listar(pedidos: list) -> int:
        if len(pedidos) == 0:
            print('Digite "0" (zero) para sair')
            print('Nenhum pedido cadastrado\n')
        else:
            print(' | '.join(['      ID      ', '     Data     ', '     Valor     ', '     Status     ']))
            for pedido in pedidos:
                print(f'#{pedido["id"]} - {pedido["data"].strftime("%d/%m/%Y")} - R${pedido["valor"]} - {pedido["status"].descricao()}')
            print('Digite "0" (zero) para sair')
            print('Digite o ID do produto para mais opções')
        return input_int(minimo=0, maximo=len(pedidos))

    @staticmethod
    def detalhes(pedido: dict) -> int:
        print('###         Pedido         ###')
        print(f'ID: {pedido["id"]}')
        print(f'Data: {pedido["data"]}')
        print(f'Status: {pedido["status"].descricao()}')
        print(f'Valor: {pedido["valor"]}')

        print('Escolha uma opção:')
        if pedido['status'] == StatusPedidoEnum.PENDENTE:
            return input_int('[1] Assumir - [0] Voltar\n')
        return input_int('[0] Voltar\n')

    @staticmethod
    def assumir() -> bool:
        print('Pedido assumido.')
        return input_int('Finalizar pedido? [1] Sim - [0] Não\n') == 1

    @staticmethod
    def sem_pedidos():
        print('Não há pedidos cadastrados.')
        input('Pressione enter para continuar...')
