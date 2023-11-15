from datetime import date, datetime
from typing import Union

from pydantic import BaseModel, Field


class Appointment(BaseModel):
    id: int = Field(gt=0)
    client_id: int
    appointment_date: Union[datetime, None]
    doctor_name: str
    notified: bool = False
    reason: str

    class Config:
        orm_mode = True


class Client(BaseModel):
    id: int = Field(gt=0)
    first_name: str = Field(min_length=3)
    cellphone: str
    identification: str = Field(min_length=3)
    identification_type: str
    date_of_birth: Union[date, None] = None
    appointments: list[Appointment]
    last_name: Union[str, None] = None

    class Config:
        orm_mode = True
