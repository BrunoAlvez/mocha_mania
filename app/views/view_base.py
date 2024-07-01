from abc import ABC

import PySimpleGUI as sg


class ViewBase(ABC):
    def __init__(self, screens: dict):
        self.__layout_atual_key = None
        self.__screens = screens

        sg.theme('DarkAmber')

        layout = []
        layout_keys = []
        for key, screen in self.__screens.items():
            key = self.key_layout(key)
            layout_keys.append(key)
            layout.append(sg.Column(
                screen,
                key=key,
                visible=len(layout) == 0,
                justification='center',
                element_justification='center',
            ))
        layout = [layout]

        self.__layout_atual_key = layout_keys[0]
        window = sg.Window(
            'Mocha Mania',
            layout=layout,
            size=(800, 600),
            resizable=True,
            finalize=True,
            element_justification='center',
        )
        while True:
            self.tratar_componentes(window)
            event, values = window.read()
            if event in (None, '-SAIR-'):
                break
            else:
                event = event.split('BUTTON-')[0] if '-BUTTON-' in event else event
                evento_tratado = self.tratar_eventos(event, values, window)
                if evento_tratado:
                    event = evento_tratado

                if event != self.__layout_atual_key and event in layout_keys:
                    window[self.__layout_atual_key].update(visible=False)
                    self.__layout_atual_key = event
                    window[self.__layout_atual_key].update(visible=True)
        window.close()

    @property
    def layout_atual_key(self):
        return self.__layout_atual_key

    @layout_atual_key.setter
    def layout_atual_key(self, layout_atual_key):
        self.__layout_atual_key = layout_atual_key

    def tratar_componentes(self, window: sg.Window):
        self.__screens[self.key_screen(self.layout_atual_key)].tratar_componentes(window, self.layout_atual_key)

    def tratar_eventos(self, event: str, values: dict, window: sg.Window):
        return self.__screens[self.key_screen(self.layout_atual_key)].tratar_eventos(event, values, window)

    @staticmethod
    def key_layout(key: str) -> str:
        return f'-{key}-'

    @staticmethod
    def key_screen(key: str) -> str:
        return key[1:-1]
