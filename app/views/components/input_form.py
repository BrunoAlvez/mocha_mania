import PySimpleGUI as sg

from app.views.components.widget import Widget


class InputForm(Widget):
    def __init__(
            self,
            text: str,
            key: str = None,
            width: int = 36,
            height: int = 0,
            font: str = 'Helvetica',
            enable_events: bool = False,
            password: bool = False,
            valor_inicial: str = None
    ):
        self.__text = text
        self.__key = key
        self.__width = width
        self.__height = height
        self.__font = font
        self.__enable_events = enable_events
        self.__password = password
        self.__valor_inicial = valor_inicial

    def builder(self) -> list:
        return [
            [sg.Text(
                f'{self.__text}:',
                key=f'-LABEL{self.__key}',
                size=(self.__width, self.__height),
                justification='left',
                font=self.__font
            )],
            [sg.Input(
                default_text=self.__valor_inicial,
                key=self.__key,
                size=(self.__width, self.__height),
                font=self.__font,
                enable_events=self.__enable_events,
                password_char='*' if self.__password else None
            )],
        ]
