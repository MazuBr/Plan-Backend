import psycopg2
from config import DB_CONF


def create_connector():
    try:
        connect = psycopg2.connect(**DB_CONF)
    except psycopg2.Error as e:
        return None
    
    return connect
