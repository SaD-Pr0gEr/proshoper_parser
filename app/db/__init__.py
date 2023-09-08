from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, DeclarativeBase

from config import config

engine = create_engine(config.db_conf.db_url)
BASE: DeclarativeBase = declarative_base()
Session = sessionmaker(bind=engine)
