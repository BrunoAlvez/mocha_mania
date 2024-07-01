import PySimpleGUI as sg

from app.controllers.estoque_controller import EstoqueController
from app.views.components.sized_box import SizedBox
from app.views.screens.screen import Screen


class EstoqueAtual(Screen):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado_id = usuario_logado_id

    def _layout(self) -> list:
        estoque_controller = EstoqueController(self.__usuario_logado_id)
        permissao_para_reabastecer = estoque_controller.verificar_permissao_para_reabastecer()
        itens = estoque_controller.listar()
        itens_lista = []
        contador = 0
        for item in itens:
            cor = '#696969' if contador % 2 == 0 else '#4F4F4F'
            quantidade = f"{item['quantidade']:.2f}".replace('.', ',')
            itens_lista.append([sg.Column([
                [
                    sg.Text(item['nome'], size=(16, 0), background_color=cor),
                    sg.Text(f"{quantidade} ({item['unidade'].descricao()})",
                            key=f'-QUANTIDADE-{item["id"]}', size=(16, 0), background_color=cor),
                    sg.Text(item['tipo'], size=(16, 0), background_color=cor),
                    sg.Input(key=f'-QUANTIDADE-{item["id"]}-INPUT-', size=(4, 0), visible=permissao_para_reabastecer),
                    sg.Button('Reabastecer', key=f'-REABASTECER-{item["id"]}-BUTTON-', size=(12, 0),
                              visible=permissao_para_reabastecer),
                ],
            ], key=f'-ITEM-{item["id"]}-COLUMN-', background_color=cor, pad=(0, 0), expand_x=True, expand_y=True,
                vertical_alignment='center', justification='center', element_justification='center')
            ])
            contador += 1

        return [
            [sg.Text('< Voltar', key='-MENU-BUTTON-', font=('Helvetica', 10), size=(0, 0), enable_events=True,
                     expand_x=True)],
            *SizedBox(height=4),
            [sg.Text('ESTOQUE', font=('Helvetica', 20, 'bold'))],
            [
                sg.Column([
                    [
                        sg.Text('Nome', size=(16, 0)),
                        sg.Text('Quantidade', size=(16, 0)),
                        sg.Text('Tipo', size=(16, 0)),
                        sg.Text('', size=(16, 0)),
                    ],
                    *itens_lista,
                ], scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True),
            ],
        ]

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if '-REABASTECER-' in event:
            item_id = int(event.split('-')[2])
            try:
                quantidade = float(values[f'-QUANTIDADE-{item_id}-INPUT-'])
            except ValueError:
                return
            item = EstoqueController(self.__usuario_logado_id).reabastecer(item_id, quantidade)
            quantidade = f"{item['quantidade']:.2f}".replace('.', ',')
            unidade = item['unidade'].descricao()
            window[f'-QUANTIDADE-{item_id}'].update(f"{quantidade} ({unidade})")
            window[f'-QUANTIDADE-{item_id}-INPUT-'].update('')
