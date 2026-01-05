from fastapi import FastAPI
from app.routers import properties


# from fastapi import Query
# from pydantic import BaseModel
import psycopg
# from psycopg.rows import dict_row
import os
from dotenv import load_dotenv

load_dotenv() # carrega as variáveis do .env 

app = FastAPI(
    title="Real Estate Listing API",
    version="0.1.0"
    )

app.include_router(properties.router)

# Função para conectar no banco
def get_conn():
   return psycopg.connect(
      host=os.getenv("DB_HOST"),
     dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
       password=os.getenv("DB_PASSWORD"),
      port=int(os.getenv("DB_PORT"))
  )

# Modelo de dados para cadastro
# class Property(BaseModel):
  #   description: str
   #  price: float
    # private_area: float
    # address: str
    # latitude: float
    # longitude: float

# Rota para cadastrar um imóvel
# @app.post("/properties")
# def create_property(property: Property):
 #    conn = get_conn()
  #   cur = conn.cursor()
   #  cur.execute(
     #    """
    #     INSERT INTO properties (description, price, private_area, address, latitude, longitude)
     #    VALUES (%(description)s, %(price)s, %(private_area)s, %(address)s, %(latitude)s, %(longitude)s)
      #   """,
       #  {
    #         "description": property.description, 
     #        "price": property.price, 
      #       "private_area": property.private_area, 
       #      "address": property.address, 
        #     "latitude": property.latitude, 
         #    "longitude": property.longitude
       #  }
    # )

    # conn.commit()
    # cur.close()
    # conn.close()
    # return {"message": "Imóvel cadastrado com sucesso!"}

# Rota para listar imóveis
# @app.get("/properties")
# def list_property(
# #     min_price: float = Query(None, description="Preço mínimo"),
#     max_price: float = Query(None, description="Preço máximo"),
#     address: str = Query(None, description="Endereço ou parte dele")
# ):
#     conn = get_conn()
#     cur = conn.cursor(row_factory=dict_row)

#     query = "SELECT id, description, price, private_area, address, creation_date, latitude, longitude FROM properties WHERE 1=1"
#     params=[]

 #    if min_price is not None:
 #        query += " AND price >= %s"
 #        params.append(min_price)

 #    if max_price is not None:
 #        query += " AND price <= %s"
 #        params.append(max_price)

  #   if address:
  #       query += " AND address ILIKE %s"
  #       params.append(f"%{address}")

  #   cur.execute(query, params)
 #    rows = cur.fetchall()
 #    cur.close()
 #    conn.close()

    # Transformar resultado em lista de dicts
   #  return rows

@app.get("/")
def healthcheck():
    return {"status": "ok"}