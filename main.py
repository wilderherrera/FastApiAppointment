from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from cron.cron_service import CronService
from database import engine
from models import models
from routes.clients import clients_routes
from routes.dates import appointments

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(appointments.router, prefix="/appointments", tags=["dates"])
app.include_router(clients_routes.router, prefix="/clients", tags=["clients"])

cron_service = CronService()


@app.on_event("startup")
@repeat_every(seconds=120, wait_first=True)
def check_client_alerts():
    cron_service.check_client_alerts()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
