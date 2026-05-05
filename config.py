import os

# Rutas de base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'aguas_moya.db')

# Asegurar que el directorio data exista
os.makedirs(DATA_DIR, exist_ok=True)
