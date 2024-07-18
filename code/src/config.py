from os import getenv
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = getenv('DATABASE_URL')

DB_CONF = {
    'dbname': getenv('PSQL_DB'),
    'user': getenv('PSQL_USER'),
    'password': getenv('PSQL_PASSWORD'),
    'host': getenv('PSQL_HOST'),
    'port': getenv('PSQL_PORT'),
}

DATABASE_URL_TEST = f"postgresql://{DB_CONF['user']}:{DB_CONF['password']}@{DB_CONF['host']}:{DB_CONF['port']}/{DB_CONF['dbname']}"


SECRET_KEY = getenv("TOKEN_SECRET_KEY")
ALGORITHM = getenv("TOKEN_ALGORITHM")

PORT = int(getenv("PORT", 8000))
