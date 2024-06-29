from app.controllers.sistema_controller import SistemaController
from database.seeders.database_seeder import DatabaseSeeder

if __name__ == '__main__':
    # Executar na primeira vez que o sistema for executado.
    # DatabaseSeeder()

    SistemaController().menu()
