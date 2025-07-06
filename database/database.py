import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from models.clients_model import Clients

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
