from app.core.database import get_conn

try:
    conn = get_conn()
    print("✅ Conectou no banco!")
    conn.close()
except Exception as e:
    print("❌ Erro ao conectar:", e)