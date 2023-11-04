from fastapi import FastAPI

from models import models
from routes.clients import clients_routes
from routes.dates import appointments
from database import engine

app = FastAPI()




models.Base.metadata.create_all(bind=engine)

app.include_router(appointments.router, prefix="/appointments", tags=["dates"])
app.include_router(clients_routes.router, prefix="/clients", tags=["clients"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
