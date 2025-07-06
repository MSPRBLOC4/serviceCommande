import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models.clients_model import Clients

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

test_engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False}, echo=True)

try:
    with engine.connect() as conn:
        print("Connexion réussie à PostgreSQL !")
except Exception as e:
    print("Erreur :", e)
