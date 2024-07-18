from src.database.conn.db import engine, meta
meta.create_all(engine)