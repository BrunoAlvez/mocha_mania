from database.seeders.cliente_seeder import ClienteSeeder
from database.seeders.funcionario_gerente_seeder import FuncionarioGerenteSeeder
from database.seeders.itens_seeder import ItensSeeder


class DatabaseSeeder:
    def __init__(self):
        seeders = [
            ClienteSeeder,
            FuncionarioGerenteSeeder,
            ItensSeeder,
        ]
        for seeder in seeders:
            for modelo in seeder.run():
                modelo.create()
