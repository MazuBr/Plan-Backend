from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_CONF = {
    'dbname': getenv('PSQL_DB'),
    'user': getenv('PSQL_USER'),
    'password': getenv('PSQL_PASSWORD'),
    'host': getenv('PSQL_HOST'),
    'port': getenv('PSQL_PORT'),
}

SECRET_KEY = getenv("TOKEN_SECRET_KEY")
ALGORITHM = getenv("TOKEN_ALGORITHM")