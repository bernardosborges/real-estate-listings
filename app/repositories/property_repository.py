from app.core.database import get_conn

def create_property_repository(data):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO properties
        (description, price, private_area, address, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            data.description,
            data.price,
            data.private_area,
            data.address,
            data.latitude,
            data.longitude
        )
    )

    conn.commit()
    cur.close()
    conn.close()


def list_properties_repository(filters: dict):
    print(">>> ENTROU NO REPOSITORY")
    conn = get_conn()
    print(">>> CONECTOU NO BANCO")
    cur = conn.cursor()
    print(">>> CRIOU CURSOR")

    query = "SELECT * FROM properties WHERE 1=1"
    params = []

    if filters.get("min_price"):
        query += " AND price >= %s"
        params.append(filters["min_price"])

    if filters.get("max_price"):
        query += " AND price <= %s"
        params.append(filters["max_price"])

    cur.execute(query, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows