import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL")

engine: Engine = create_engine(DATABASE_URL, echo=True)

Session: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base: type = declarative_base()
