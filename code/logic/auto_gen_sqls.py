from psycopg2 import sql

def auto_gen(data: dict, query: str):
    columns = data.keys()
    placeholders = [f"%({column})s" for column in columns]
    result = sql.SQL(query.format(
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        values=sql.SQL(', ').join(map(sql.SQL, placeholders))
    ))
    print('auto_gen_sqls. str 9. sql query after autocreate query: ', result)
    return result