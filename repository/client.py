from sqlalchemy.orm import Session

from models import models


def get_client_by_id(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_client_by_document(db: Session, identification_type: str, identification: str):
    return db.query(models.Client).filter(models.Client.identification_type.ilike(identification_type),
                                          models.Client.identification == identification).first()


def get_all_clients(db: Session):
    return db.query(models.Client).all()
