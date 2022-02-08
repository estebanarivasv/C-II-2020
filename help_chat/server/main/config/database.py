import os
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DB_URI = os.getenv('DB_URI')

engine = create_engine(DB_URI, echo=True, future=True)
Base = declarative_base()
