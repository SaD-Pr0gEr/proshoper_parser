from sqlalchemy import create_engine, Connection, Engine
from sqlalchemy.orm import declarative_base, sessionmaker, DeclarativeBase

from config import config

engine = create_engine(config.db_conf.db_url, pool_recycle=3600)
BASE: DeclarativeBase = declarative_base()
Session = sessionmaker(bind=engine)
