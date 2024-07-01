from datetime import datetime

import PySimpleGUI as sg

import app.helpers.string as string_helper
from app.controllers.cliente_controller import ClienteController
from app.views.components.sized_box import SizedBox
from app.views.screens.screen import Screen


class Perfil(Screen):
    def __init__(self, usuario_logado_id: int):
        self.__usuario_logado_id = usuario_logado_id

    def _layout(self) -> list:
        cliente = ClienteController(self.__usuario_logado_id).perfil()
        if isinstance(cliente['data_de_nascimento'], str):
            cliente['data_de_nascimento'] = datetime.strptime(cliente['data_de_nascimento'], '%d/%m/%Y')
        return [
            [sg.Text('< Voltar', key='-MENU-BUTTON-', font=('Helvetica', 10), size=(0, 0), enable_events=True,
                     expand_x=True)],
            [sg.Text('Perfil')],
            [
                sg.Text('Nome:', size=(12, 0)),
                sg.Text(cliente['nome'], key='-NOME-', colors='white', size=(16, 0)),
            ],
            [
                sg.Text('E-mail:', size=(12, 0)),
                sg.Text(cliente['email'], key='-EMAIL-', colors='white', size=(16, 0)),
            ],
            [
                sg.Text('CPF:', size=(12, 0)),
                sg.Text(cliente['cpf'], key='-CPF-', colors='white', size=(16, 0)),
            ],
            [
                sg.Text('Telefone:', size=(12, 0)),
                sg.Text(cliente['telefone'], key='-TELEFONE-', colors='white', size=(16, 0)),
            ],
            [
                sg.Text('Data de nascimento:', size=(12, 0)),
                sg.Text(string_helper.formatar_data(cliente['data_de_nascimento']), key='-DATA-DE-NASCIMENTO-',
                        colors='white', size=(16, 0)),
            ],
            *SizedBox(height=4),
            *self.__secao_fidelidade(cliente),
            [sg.Text('Atualizar dados', key='-ATUALIZAR-PERFIL-BUTTON-', font=('Helvetica', 10), size=(0, 0),
                     enable_events=True)],
            [sg.Text('Remover conta', key='-REMOVER-BUTTON-', font=('Helvetica', 10), size=(0, 0), enable_events=True)],
            *SizedBox(height=4),
        ]

    @staticmethod
    def __secao_fidelidade(cliente: dict) -> list:
        fidelizado = True if cliente['fidelidade'] else False
        fidelidade = cliente['fidelidade']
        pontos = fidelidade['pontos'] if fidelizado else ''
        classificacao = fidelidade['classificacao'] if fidelizado else ''
        return [
            [sg.Column(
                [
                    [
                        sg.Text('Pontos:', size=(12, 0)),
                        sg.Text(pontos, key='-PONTOS-', colors='white', size=(16, 0))
                    ],
                    [
                        sg.Text('Classificação:', size=(12, 0)),
                        sg.Text(classificacao, key='-CLASSIFICACAO-', colors='white', size=(16, 0)),
                    ],
                ],
                key='-FIDELIDADE-COLUMN-',
                visible=fidelizado,
            )],
            [
                sg.Button(
                    'Fidelizar',
                    key='-FIDELIZAR-BUTTON-',
                    font=('Helvetica', 10),
                    size=(16, 0),
                    visible=not fidelizado,
                ),
            ],
        ]

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        if event == '-REMOVER-':
            retorno = sg.popup_ok_cancel('Deseja realmente remover a conta?')
            if retorno == 'OK':
                from app.views.sistema_view import SistemaView
                ClienteController(self.__usuario_logado_id).remover()
                window.hide()
                SistemaView()
        elif event == '-FIDELIZAR-':
            fidelidade = ClienteController(self.__usuario_logado_id).fidelizar()
            window['-FIDELIZAR-BUTTON-'].update(visible=False)
            window['-FIDELIDADE-COLUMN-'].update(visible=True)
            window['-PONTOS-'].update(fidelidade['pontos'])
            window['-CLASSIFICACAO-'].update(fidelidade['classificacao'])
