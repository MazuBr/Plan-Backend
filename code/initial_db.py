from src.database.conn.db import engine, meta, conn
from src.database.models.users import *
from src.database.models.calendar import calendar
from sqlalchemy import event, select

meta.drop_all(engine)
    
meta.create_all(engine)

conn.execute(roles.insert().values(name='admin'))
conn.execute(roles.insert().values(name='user'))
conn.execute(roles.insert().values(name='demo'))

conn.execute(default_role_sql)
