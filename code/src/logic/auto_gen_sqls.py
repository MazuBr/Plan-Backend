from psycopg2 import sql

def auto_gen(data: dict, query: str) -> sql.SQL:
    columns = data.keys()
    placeholders = [f"%({column})s" for column in columns]
    result = sql.SQL(query).format(
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        values=sql.SQL(', ').join(sql.SQL(placeholder) for placeholder in placeholders)
    )
    return result
