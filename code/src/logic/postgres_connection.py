from typing import Any, Dict, List

from psycopg2 import connect, DatabaseError, IntegrityError, errors
from psycopg2.extensions import connection as Connection, cursor as Cursor
from psycopg2.extras import RealDictCursor

from src.config import DB_CONF


class Database:
    def __init__(self):
        self.connection: Connection = connect(**DB_CONF)
        self.cursor: Cursor = self.connection.cursor(cursor_factory=RealDictCursor)
    
    def fetch_all(self, query: str, params: dict = None) -> list[dict]|errors.UniqueViolation|None:
        try:
            if params:
                self.cursor.execute(query=query, vars=params)
            else:
                self.cursor.execute(query=query)
            results: List[Dict[str, Any]] = self.cursor.fetchall()
            self.commit()

            return results
        
        except errors.UniqueViolation as unique_error:
            self.connection.rollback()
            return unique_error
        
        except (Exception, DatabaseError, IntegrityError) as error:
            self.connection.rollback()
            return 'Server error'
        
        finally:
            self.close()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
