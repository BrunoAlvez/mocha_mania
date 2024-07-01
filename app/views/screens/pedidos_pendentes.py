import PySimpleGUI as sg

from app.controllers.pedido_controller import PedidoController
from app.views.components.sized_box import SizedBox
from app.views.screens.screen import Screen


class PedidosPendentes(Screen):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado_id = usuario_logado_id

    def _layout(self) -> list:
        pedidos = PedidoController(self.__usuario_logado_id).listar({'apenas_pendentes': True})
        if len(pedidos) == 0:
            return [
                [sg.Text('< Voltar', key='-MENU-BUTTON-', font=('Helvetica', 10), size=(0, 0), enable_events=True,
                         expand_x=True)],
                [sg.Text('Sem pedidos pendentes')],
            ]

        pedidos_lista = []
        contador = 0
        for pedido in pedidos:
            cor = '#696969' if contador % 2 == 0 else '#4F4F4F'
            responsavel = pedido['responsavel']['nome'] if pedido['responsavel'] is not None else 'Nenhum'
            pedidos_lista.append([sg.Column([
                [
                    sg.Text(pedido['cliente']['nome'], key=f'-CLIENTE-{pedido["id"]}', size=(16, 0),
                            background_color=cor),
                    sg.Text(pedido['status'].descricao(), key=f'-STATUS-{pedido["id"]}', size=(16, 0),
                            background_color=cor),
                    sg.Text(responsavel, key=f'-RESPONSAVEL-{pedido["id"]}', size=(16, 0), background_color=cor),
                    sg.Button('Assumir', key=f'-ASSUMIR-{pedido["id"]}-BUTTON-', size=(16, 0),
                              visible=pedido['responsavel'] is None),
                    sg.Button('Finalizar', key=f'-FINALIZAR-{pedido["id"]}-BUTTON-', size=(16, 0),
                              visible=pedido['responsavel'] is not None),
                ],
            ], key=f'-PEDIDO-{pedido["id"]}-COLUMN-', background_color=cor, pad=(0, 0), expand_x=True, expand_y=True,
                vertical_alignment='center', justification='center', element_justification='center')
            ])
            contador += 1
        return [
            [sg.Text('< Voltar', key='-MENU-BUTTON-', font=('Helvetica', 10), size=(0, 0), enable_events=True,
                     expand_x=True)],
            *SizedBox(height=4),
            [sg.Text('PEDIDOS', font=('Helvetica', 20, 'bold'))],
            [
                sg.Text('Cliente', size=(16, 0)),
                sg.Text('Status', size=(16, 0)),
                sg.Text('Responsável', size=(16, 0)),
                sg.Text('', size=(16, 0)),
            ],
            [
                sg.Column([
                    *pedidos_lista,
                ], scrollable=True, vertical_scroll_only=True, size=(800, 400)),
            ],
        ]

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if '-ASSUMIR-' in event:
            pedido_id = int(event.split('-')[2])
            pedido = PedidoController(self.__usuario_logado_id).assumir(pedido_id)
            window['-ASSUMIR-{}-BUTTON-'.format(pedido_id)].update(visible=False)
            window['-FINALIZAR-{}-BUTTON-'.format(pedido_id)].update(visible=True)
            window['-RESPONSAVEL-{}'.format(pedido_id)].update(value=pedido['responsavel']['nome'])
            window['-STATUS-{}'.format(pedido_id)].update(value=pedido['status'].descricao())
        elif '-FINALIZAR-' in event:
            pedido_id = int(event.split('-')[2])
            PedidoController(self.__usuario_logado_id).finalizar(pedido_id)
            window['-PEDIDO-{}-COLUMN-'.format(pedido_id)].update(visible=False)
