from app.enums.enum_base import EnumBase


class UnidadeEnum(EnumBase):
    MILIGRAMA = 'miligrama'
    GRAMA = 'grama'
    QUILOGRAMA = 'quilograma'
    MILILITRO = 'mililitro'
    LITRO = 'litro'
    COLHER_SOPA = 'colher_sopa'
    COLHER_CHA = 'colher_cha'
    XICARA = 'xicara'
    UNIDADE = 'unidade'

    def descricao(self):
        return {
            self.MILIGRAMA: 'Miligrama',
            self.GRAMA: 'Grama',
            self.QUILOGRAMA: 'Quilograma',
            self.MILILITRO: 'Mililitro',
            self.LITRO: 'Litro',
            self.COLHER_SOPA: 'Colher de sopa',
            self.COLHER_CHA: 'Colher de chá',
            self.XICARA: 'Xícara',
            self.UNIDADE: 'Unidade',
        }[self]

    def sigla(self):
        return {
            self.MILIGRAMA: 'mg',
            self.GRAMA: 'g',
            self.QUILOGRAMA: 'kg',
            self.MILILITRO: 'ml',
            self.LITRO: 'l',
            self.COLHER_SOPA: 'cs',
            self.COLHER_CHA: 'cc',
            self.XICARA: 'xíc',
            self.UNIDADE: 'un'
        }[self]
