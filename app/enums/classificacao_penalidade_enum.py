from app.enums.enum_base import EnumBase


class ClassificacaoPenalidadeEnum(EnumBase):
    DIAMANTE = 'diamante'
    OURO = 'ouro'
    PRATA = 'prata'
    BRONZE = 'bronze'

    def descricao(self):
        return {
            self.DIAMANTE: 'Diamante',
            self.OURO: 'Ouro',
            self.PRATA: 'Prata',
            self.BRONZE: 'Bronze',
        }[self]

    def minimo_de_pontos(self):
        return {
            self.DIAMANTE: 1000,
            self.OURO: 500,
            self.PRATA: 200,
            self.BRONZE: 0,
        }[self]
