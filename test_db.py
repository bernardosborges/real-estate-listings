import psycopg

conn = psycopg.connect(
    host="realestatelistings-postgres.c45omgqa23v0.us-east-1.rds.amazonaws.com",
    dbname="realestatelistings",
    user="postgresadmin",
    password="AfErHYtG5As",
    port=5432
)

print "Conectado com sucesso!"
conn.close()