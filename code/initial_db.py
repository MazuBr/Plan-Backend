from sqlalchemy import text

from src.database.conn.db import engine, meta, conn
from src.database.models.users import roles, users, default_role_sql
from src.database.models.calendar import calendar, calendar_user_association

meta.drop_all(engine)

drop_all_triggers = text("""
DO $$ 
DECLARE 
    r RECORD;
BEGIN
    FOR r IN (SELECT trigger_name, event_object_table 
              FROM information_schema.triggers) 
    LOOP
        EXECUTE 'DROP TRIGGER ' || quote_ident(r.trigger_name) || ' ON ' || quote_ident(r.event_object_table);
    END LOOP;
END $$;
""")

drop_all_functions = text("""
DO $$ 
DECLARE 
    r RECORD;
BEGIN
    FOR r IN (SELECT routine_name 
              FROM information_schema.routines 
              WHERE routine_type='FUNCTION' AND specific_schema='public') 
    LOOP
        EXECUTE 'DROP FUNCTION ' || quote_ident(r.routine_name) || '()';
    END LOOP;
END $$;
""")


meta.create_all(engine)

conn.execute(roles.insert().values(name='admin'))
conn.execute(roles.insert().values(name='user'))
conn.execute(roles.insert().values(name='demo'))

conn.execute(drop_all_triggers)
conn.execute(drop_all_functions)
