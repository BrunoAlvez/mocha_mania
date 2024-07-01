import PySimpleGUI as sg

from app.views.components.widget import Widget


class SizedBox(Widget):
    def __init__(self, key: str = '', width: int = 0, height: int = 0):
        self.__key = key
        self.__width = width
        self.__height = height

    def builder(self) -> list:
        return [[sg.Text('', key=self.__key, size=(self.__width, self.__height))]]
