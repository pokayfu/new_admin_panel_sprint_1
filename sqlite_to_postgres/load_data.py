def load_from_sqlite(curs, table_name: str):
    curs.execute(f"SELECT * FROM {table_name};")
    data = curs.fetchall()
    return data
