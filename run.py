import os
from init_db import create_db
from src import create_app

if __name__ == '__main__':
    if not os.path.exists(os.environ.get('DB_PATH', '/data/database.db')):
        print("Database SQLite não encontrada. Criando-a a partir de dados web...")
        create_db()

    app = create_app()
    app.run(host='0.0.0.0', port=5000)