import PySimpleGUI as sg

import app.helpers.string as string_helper
from app.controllers.cliente_controller import ClienteController
from app.controllers.estoque_controller import EstoqueController
from app.views.components.sized_box import SizedBox
from app.views.screens.screen import Screen


class MenuPedidoCliente(Screen):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado_id = usuario_logado_id

    def _layout(self) -> list:
        itens = EstoqueController().listar_produtos()
        itens_lista = []
        contador = 0
        for item in itens:
            cor = '#696969' if contador % 2 == 0 else '#4F4F4F'
            itens_lista.append([sg.Column([
                [
                    sg.Button('', size=(2, 0), key=f'-PEDIDO-PRODUTO-{item["id"]}-BUTTON-',
                              button_color=('white', cor)),
                    sg.Text(item['nome'], size=(48, 0), background_color=cor),
                    sg.Text(string_helper.formatar_preco(item['preco']), size=(8, 0), justification='center',
                            background_color=cor),
                    sg.Text('Disponível' if item['disponivel'] else 'Indisponível', size=(16, 0),
                            justification='center', background_color=cor),
                ],
            ], key=f'-PEDIDO-{item["id"]}-COLUMN-', background_color=cor, pad=(0, 0), expand_x=True, expand_y=True,
                vertical_alignment='center', justification='center', element_justification='center')
            ])
            contador += 1
        return [
            [sg.Text('< Voltar', key='-MENU-BUTTON-', font=('Helvetica', 10), size=(0, 0), enable_events=True,
                     expand_x=True)],
            *SizedBox(height=4),
            [sg.Text('CARDÁPIO', font=('Helvetica', 20, 'bold'))],
            [
                sg.Text('Nome', size=(48, 0)),
                sg.Text('Preço', size=(8, 0), justification='center'),
                sg.Text('Disponibilidade', size=(16, 0), justification='center'),
            ],
            [
                sg.Column([
                    *itens_lista,
                ], scrollable=True, vertical_scroll_only=True, size=(800, 400)),
            ],
        ]

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if event.startswith('-PEDIDO-PRODUTO-'):
            produto_id = int(event.split('-')[-2])
            retorno = ClienteController(self.__usuario_logado_id).pedir(produto_id)
            if isinstance(retorno, dict):
                try:
                    pontos_fidelidade = retorno['cliente']['fidelidade']['pontos']
                    window['-PONTOS-'].update(pontos_fidelidade)
                except KeyError:
                    pass
                except TypeError:
                    pass
                return '-MENU-'
            else:
                sg.popup('Erro ao realizar pedido!', 'Produto indisponível ou não encontrado.')
