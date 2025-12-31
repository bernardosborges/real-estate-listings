import psycopg

# Conexão com RDS
conn = psycopg.connect(
    host="realestatelistings-postgres.c45omgqa23v0.us-east-1.rds.amazonaws.com",
    dbname="realestatelistings",
    user="postgresadmin",
    password="AfErHYtG5As",
    port=5432
)

# Cria um cursor
cur = conn.cursor()

# Comando SQL para criar tabela
create_table_query = """
CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    description TEXT,
    price NUMERIC(12,2),
    address VARCHAR(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Executa o comando
cur.execute(create_table_query)
conn.commit()

print("Tabela 'properties' criada com sucesso!")

# Fecha a conexão
cur.close()
conn.close()
