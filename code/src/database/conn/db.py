from sqlalchemy import create_engine, MetaData
from src.config import DATABASE_URL 
engine = create_engine(DATABASE_URL)
meta = MetaData()

conn = engine.connect()