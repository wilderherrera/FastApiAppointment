import locale
from datetime import datetime

from fastapi import Depends, APIRouter, Path, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import repository.appointment
import repository.client
import squemas.squemas
from database import SessionLocal
from utils.utils import Utils

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

utils = Utils()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


def build_appointment_message_one(appointment, message):
    result = f"Esta es tu cita {message}:\n"
    result += f"*Fecha de la cita:* {utils.format_date(appointment.appointment_date)}\n"
    result += f"*Nombre del doctor:* {appointment.doctor_name}\n"
    result += f"*Razón de la cita:* {appointment.reason}\n\n"
    return result


def build_appointment_message(appointments, message):
    result = f"Estas son tus citas {message}:\n"

    for index, cita in enumerate(appointments, start=1):
        result += f"*{index}. Fecha de la cita:* {datetime.fromisoformat(str(cita.appointment_date)).strftime('%A, %d de %B de %Y a las %I:%M %p')}\n"
        result += f"*Nombre del doctor:* {cita.doctor_name}\n"
        result += f"*Razón de la cita:* {cita.reason}\n\n"
    return result


@router.get("", response_model=list[squemas.squemas.Client], status_code=status.HTTP_200_OK)
async def get_all_clients(db: Session = Depends(get_db)):
    return repository.client.get_all_clients(db)


@router.get("/{client_id}", response_model=squemas.squemas.Client, status_code=status.HTTP_200_OK)
async def get_client_by_id(client_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return repository.client.get_client_by_id(db, client_id)


@router.get("/identification/{identification_type}/{identification}/available",
            response_model=list[squemas.squemas.Appointment],
            status_code=status.HTTP_200_OK)
async def get_client_by_id(identification_type: str = Path(min_length=1), identification: str = Path(min_length=3),
                           db: Session = Depends(get_db)):
    appointments = repository.appointment.get_all_appointments_by_client_identification(db, identification_type,
                                                                                        identification)
    if appointments is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado con los parametros de busqueda")
    return appointments


@router.get("/identification/{identification_type}/{identification}/taken/render",
            status_code=status.HTTP_200_OK)
async def get_client_by_id_rendered(identification_type: str = Path(min_length=1),
                                    identification: str = Path(min_length=3),
                                    db: Session = Depends(get_db)):
    appointments = repository.appointment.get_all_appointments_by_client_identification(db,
                                                                                        identification_type,
                                                                                        identification, True)
    if len(appointments) == 0:
        return {"api_message": "No tienes citas programadas"}

    build_appointment_message(appointments, "agendadas")

    if appointments is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado con los parametros de busqueda")
    return {"api_message": build_appointment_message(appointments, "agendadas")}


@router.get("/identification/{identification_type}/{identification}/available/render",
            status_code=status.HTTP_200_OK)
async def get_client_by_id_rendered(identification_type: str = Path(min_length=1),
                                    identification: str = Path(min_length=3),
                                    db: Session = Depends(get_db)):
    appointments = repository.appointment.get_all_appointments_by_client_identification(db,
                                                                                        identification_type,
                                                                                        identification)
    if len(appointments) == 0:
        return {"api_message": "No tienes citas disponibles"}

    if appointments is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado con los parametros de busqueda")
    return {"api_message": build_appointment_message(appointments, "disponibles")}


@router.get("/identification/{identification_type}/{identification}/available/selected/{appointment_index}/render",
            status_code=status.HTTP_200_OK)
async def get_client_by_id_rendered(identification_type: str = Path(min_length=1),
                                    identification: str = Path(min_length=3),
                                    appointment_index: int = Path(min=1),
                                    db: Session = Depends(get_db)):
    appointments = repository.appointment.get_all_appointments_by_client_identification(db,
                                                                                        identification_type,
                                                                                        identification)
    selected_appointment = appointments[appointment_index - 1]

    if selected_appointment is None:
        return {"api_message": "No tienes citas disponibles"}

    if appointments is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado con los parametros de busqueda")
    return {"api_message": build_appointment_message_one(selected_appointment, "seleccionada"),
            "appointment_id": selected_appointment.id}


@router.get("/identification/{identification_type}/{identification}", response_model=squemas.squemas.Client,
            status_code=status.HTTP_200_OK)
async def get_client_by_id(identification_type: str = Path(min_length=1), identification: str = Path(min_length=3),
                           db: Session = Depends(get_db)):
    client = repository.client.get_client_by_document(db, identification_type, identification)
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado con los parametros de busqueda")
    return client
