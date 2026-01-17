

def create_updated_at_trigger(tables: list[str]) -> str:
    
    sql = """
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
       NEW.updated_at = now();
       RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """

    for table in tables:
        sql += f"""
        DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};
        CREATE TRIGGER update_{table}_updated_at
        BEFORE UPDATE ON {table}
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
        """

    return sql