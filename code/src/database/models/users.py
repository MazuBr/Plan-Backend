from sqlalchemy import Column, Integer, String, Table, Sequence,\
     BigInteger, ForeignKey, Text, Boolean, text

from src.database.conn.db import meta
import time 

roles = Table('roles', meta,
                    Column('id', Integer, Sequence('roles_id_seq', start=1, increment=1), primary_key=True),
                    Column('name', String(50), unique=True, nullable=False))

users = Table(
    'users', meta,
    Column('id', BigInteger, Sequence('user_id_seq'), primary_key=True),
    Column('username', String(50), unique=True, nullable=False),
    Column('role', Integer, ForeignKey('roles.id'), default=None),
    Column('email', String(100), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('first_name', String(100)),
    Column('last_name', String(100)),
    Column('phone', String(20)),
    Column('address', Text),
    Column('created_at', BigInteger, default=lambda: int(time.time())),
    Column('updated_at', BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time())),
    Column('is_deleted', Boolean, default=False),
    Column('deleted_at', BigInteger, nullable=True)
)

default_role_sql = text('''
CREATE OR REPLACE FUNCTION set_default_role()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.role IS NULL THEN
        NEW.role := (SELECT id FROM roles WHERE name = 'user');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_default_role_trigger
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION set_default_role();
''')
