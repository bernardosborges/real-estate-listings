from sqlalchemy.orm import Session
from app.models.property_model import PropertyModel
from app.schemas.property_schema import PropertyCreateSchema


def create_property(db: Session, schema: PropertyCreateSchema):
    data = schema.model_dump() # exclude={"tags_ids"}
    db_property = PropertyModel(**data)
    
    print(">>> ENTROU NO REPOSITORY")
    db.add(db_property)
    print(">>> ADDED PROPERTY")
    db.commit()
    print(">>> COMMITED")
    db.refresh(db_property)
    return db_property

def list_properties(db: Session):
    return db.query(PropertyModel).all()





# from app.core.database import get_conn


# # =====================================================
# # CREATE PROPERTY (MODO MANUAL SEM SESSION)
# # =====================================================

# def create_property_repository(data):
#     conn = get_conn()
#     cur = conn.cursor()

#     cur.execute(
#         """
#         INSERT INTO properties
#         (
#             description,
#             price,
#             private_area,
#             address,
#             latitude,
#             longitude
#         )
#         VALUES (%s, %s, %s, %s, %s, %s)
#         RETURNING id
#         """,
#         (
#             data.description,
#             data.price,
#             data.private_area,
#             data.address,
#             data.latitude,
#             data.longitude
#         )
#     )

#     # Pega o ID gerado pelo banco
#     property_id = cur.fetchone()[0]

#     # Confirma a transação
#     conn.commit()
    
#     cur.close()
#     conn.close()

#     return property_id


# # =====================================================
# # LIST PROPERTIES (WITH FILTERS) (MODO MANUAL SEM SESSION)
# # =====================================================

# def list_properties_repository(filters: dict):
#     print(">>> ENTROU NO REPOSITORY")
#     conn = get_conn()
#     print(">>> CONECTOU NO BANCO")
#     cur = conn.cursor()
#     print(">>> CRIOU CURSOR")

#     # Base da query (WHERE 1=1 facilita filtros opcionais)
#     query = "SELECT * FROM properties WHERE 1=1"
#     params = []

#     # Filtro: preço mínimo
#     if filters.get("min_price") is not None:
#         query += " AND price >= %s"
#         params.append(filters["min_price"])

#     # Filtro: preço máximo
#     if filters.get("max_price") is not None:
#         query += " AND price <= %s"
#         params.append(filters["max_price"])

#     # Executa query com parâmetros
#     cur.execute(query, params)

#     # Captura nome das colunas
#     columns = [desc[0] for desc in cur.description]

#     # Busca dados
#     rows = cur.fetchall()

#     # Transforma lista de tuplas em lista de dicionários
#     result = [
#         dict(zip(columns, row))
#         for row in rows
#     ]

#     cur.close()
#     conn.close()
#     return result