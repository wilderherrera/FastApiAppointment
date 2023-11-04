from sqlalchemy import Boolean,Date, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    identification = Column(String, unique=True, index=True)
    identification_type = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    appointments = relationship("Appointment", back_populates="client")


class Appointment(Base):
    __tablename__ = "appointments"
    id: int = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    appointment_date = Column(Date)
    doctor_name = Column(String)
    taken = Column(Boolean)
    reason = Column(String)
    client = relationship("Client", back_populates="appointments")
