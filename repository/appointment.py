from sqlalchemy import or_
from sqlalchemy.orm import Session

from models import models


def get_all_appointment(db: Session):
    return db.query(models.Appointment).all()


def get_appointment_by_id(db: Session, appointment_id: int) -> models.Appointment:
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()


def get_all_appointment_available(db: Session) -> list[models.Appointment]:
    return db.query(models.Appointment).filter(models.Appointment.taken == False).all()


def get_all_appointment_taken_and_notification_pending(db: Session) -> list[models.Appointment]:
    return db.query(models.Appointment).filter(models.Appointment.taken).filter(
        or_(models.Appointment.notified == False, models.Appointment.notified is None)).all()


def get_all_appointments_by_client_identification(db: Session, identification_type: str, identification: str,
                                                  taken=False) -> list[models.Appointment]:
    return db.query(models.Appointment).join(models.Client).filter(
        models.Appointment.taken == taken,
        models.Client.identification_type.ilike(identification_type),
        models.Client.identification == identification).order_by(models.Appointment.id).all()
