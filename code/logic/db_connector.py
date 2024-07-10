from typing import Any, Dict, List

from psycopg2 import connect, DatabaseError, IntegrityError, errors
from psycopg2.extensions import connection as Connection, cursor as Cursor
from psycopg2.extras import RealDictCursor

from config import DB_CONF


class Database:
    def __init__(self):
        self.connection: Connection = connect(**DB_CONF)
        self.cursor: Cursor = self.connection.cursor(cursor_factory=RealDictCursor)
    
    def fetch_all(self, query: str, params: dict = None) -> str|None:
        try:
            if params:
                self.cursor.execute(query=query, params=params)
            else:
                self.cursor.execute(query=query)
            results: List[Dict[str, Any]] = self.cursor.fetchall()
            return results
        
        except errors.UniqueViolation as unique_error:
            self.connection.rollback()
            print('db_connector, 26: ', unique_error)
            return 'email or login already used'
        except (Exception, DatabaseError, IntegrityError) as error:
            self.connection.rollback()
            print('db_connector, 30: ', error)
            return 'Server error'
        
        finally:
            self.cursor.close()
            self.connection.close()
