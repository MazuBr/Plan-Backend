from sqlalchemy import Column, Integer, String, Table, Sequence
from sqlalchemy.sql.sqltypes import Integer, String

from src.database.conn.db import meta

roles_table = Table('roles', meta,
                    Column('id', Integer, Sequence('roles_id_seq', start=1, increment=1), primary_key=True),
                    Column('name', String(50), unique=True, nullable=False))