from app.enums.enum_base import EnumBase


class UnidadeTempoEnum(EnumBase):
    SEGUNDO = 'segundo'
    MINUTO = 'minuto'
    HORA = 'hora'

    def descricao(self):
        return {
            self.SEGUNDO: 'Segundo',
            self.MINUTO: 'Minuto',
            self.HORA: 'Hora',
        }[self]

    def sigla(self):
        return {
            self.SEGUNDO: 'seg',
            self.MINUTO: 'min',
            self.HORA: 'h',
        }[self]
