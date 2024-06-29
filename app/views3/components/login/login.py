import PySimpleGUI as sg

from app.views.components.componente import Componente


class Login(Componente):
    def _componentes(self) -> list:
        return [
            [
                sg.Column(
                    [[sg.Text(
                        'Mocha Mania',
                        key='-LOGO-',
                        font=('Helvetica', 16),
                    )]],
                    pad=((136, 0), 24),
                    expand_x=True,
                    element_justification='left',
                    size=(800, 600),
                ),
            ],
        ]
