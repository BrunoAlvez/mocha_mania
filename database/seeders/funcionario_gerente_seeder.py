from app.enums.cargo_enum import CargoEnum
from database.seeders.seeder import Seeder
from app.models.funcionario import Funcionario


class FuncionarioGerenteSeeder(Seeder):
    @staticmethod
    def run() -> [Funcionario]:
        return [Funcionario(
            id=1,
            nome='Administrador',
            login='admin',
            email='admin@email.com',
            senha='admin123',
            cargo=CargoEnum.GERENTE,
        )]
