import psycopg
from app.core.config import settings

# Função para conectar no banco
def get_conn():
    return psycopg.connect(
        host=settings.DB_HOST,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT
    )