from fastapi import FastAPI, APIRouter, Depends, Path
from sqlalchemy.orm import Session

import repository.appointment
from database import SessionLocal
from starlette import status

app = FastAPI()
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
async def get_all_appointment(db: Session = Depends(get_db)):
    return repository.appointment.get_all_appointment(db)


@router.post("/{appointment_id}/confirm/render",
             status_code=status.HTTP_200_OK)
async def post_client_by_id_rendered(appointment_id: int = Path(min=1),
                                    db: Session = Depends(get_db)):
    appointment = repository.appointment.get_appointment_by_id(db, appointment_id)
    appointment.taken = True
    db.add(appointment)
    db.commit()
    return {"api_message": "Cita confirmada exitosamente"}
