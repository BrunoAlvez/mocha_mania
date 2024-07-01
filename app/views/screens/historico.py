import PySimpleGUI as sg

import app.helpers.string as string_helper
from app.controllers.cliente_controller import ClienteController
from app.views.components.sized_box import SizedBox
from app.views.screens.screen import Screen


class Historico(Screen):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado_id = usuario_logado_id
        self.__pedidos = ClienteController(usuario_logado_id=self.__usuario_logado_id).historico()

    def _layout(self) -> list:
        pedidos = self.__pedidos
        historico_lista = []
        contador = 0
        for item in pedidos:
            cor = '#696969' if contador % 2 == 0 else '#4F4F4F'
            produtos = [produto.descricao for produto in item['itens']]
            historico_lista.append([sg.Column([
                [
                    sg.Text(', '.join(produtos), key=f'-PRODUTOS-{item["id"]}', size=(48, 0), background_color=cor),
                    sg.Text(item['status'].descricao(), key=f'-STATUS-{item["id"]}', size=(16, 0),
                            background_color=cor),
                    sg.Text(string_helper.formatar_preco(item['valor']), key=f'-VALOR-{item["id"]}', size=(8, 0),
                            justification='center', background_color=cor),
                    sg.Text(string_helper.formatar_data(item['data'], True), key=f'-DATA-{item["id"]}', size=(16, 0),
                            justification='center', background_color=cor)
                ],
            ], key=f'-PEDIDO-{item["id"]}-COLUMN-', background_color=cor, pad=(0, 0), expand_x=True, expand_y=True,
                vertical_alignment='center', justification='center', element_justification='center')])
            contador += 1
        return [
            [sg.Text('< Voltar', key='-MENU-BUTTON-', font=('Helvetica', 10), size=(0, 0), enable_events=True,
                     expand_x=True)],
            *SizedBox(height=4),
            [sg.Text('HISTÓRICO', font=('Helvetica', 20, 'bold'))],
            [
                sg.Text('Filtro por data:'),
                sg.Input(key='-DATA-INPUT-', size=(16, 0), enable_events=True, justification='center'),
                sg.Button('Filtrar', key='-FILTRAR-BUTTON-', size=(16, 0)),
            ],
            [
                sg.Text('Itens', size=(48, 0)),
                sg.Text('Status', size=(16, 0)),
                sg.Text('Valor', size=(8, 0), justification='center'),
                sg.Text('Data', size=(16, 0), justification='center'),
            ],
            [
                sg.Column([
                    *historico_lista,
                ], scrollable=True, vertical_scroll_only=True, size=(800, 400)),
            ],
        ]

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if event == '-FILTRAR-':
            data = values['-DATA-INPUT-']
            pedidos = ClienteController(usuario_logado_id=self.__usuario_logado_id).historico(data)
            pedidos_ids = [pedido['id'] for pedido in pedidos]
            for pedido in self.__pedidos:
                window[f'-PRODUTOS-{pedido["id"]}'].update(visible=pedido['id'] in pedidos_ids)
                window[f'-STATUS-{pedido["id"]}'].update(visible=pedido['id'] in pedidos_ids)
                window[f'-VALOR-{pedido["id"]}'].update(visible=pedido['id'] in pedidos_ids)
                window[f'-DATA-{pedido["id"]}'].update(visible=pedido['id'] in pedidos_ids)
                window[f'-PEDIDO-{pedido["id"]}-COLUMN-'].update(visible=pedido['id'] in pedidos_ids)
        if event == '-MENU-':
            from app.views.cliente_view import ClienteView
            window.hide()
            ClienteView(self.__usuario_logado_id)
        if event == '-DATA-INPUT-':
            window[event].update(string_helper.mascara_data(values[event]))
