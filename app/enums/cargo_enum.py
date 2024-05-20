from app.enums.enum_base import EnumBase


class CargoEnum(EnumBase):
    GERENTE = 'gerente'
    ATENDENTE = 'atendente'
    BARISTA = 'barista'

    def descricao(self):
        return {
            self.GERENTE: 'Gerente',
            self.ATENDENTE: 'Atendente',
            self.BARISTA: 'Barista',
        }[self]

    @staticmethod
    def cargo_por_id(id: int):
        return {
            1: CargoEnum.GERENTE,
            2: CargoEnum.ATENDENTE,
            3: CargoEnum.BARISTA,
        }[id]
