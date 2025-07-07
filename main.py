from fastapi import FastAPI
from routes.commandes import router as commandes_router
from database import init_db
from database.database import create_db_and_tables


app = FastAPI(title="API de Gestion des Commandes")

create_db_and_tables()

# Inclusion des routes
app.include_router(commandes_router, prefix="/commandes", tags=["Commandes"])

@app.get("/health")
def health():
    return {"status": "ok"}

from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator().instrument(app).expose(app)
