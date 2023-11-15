import repository.appointment
import repository.client
from database import SessionLocal
from message.whatsapp_message import WhatsappMessage
from utils.utils import Utils

utils = Utils()


class CronService:
    def __init__(self):
        self.db = SessionLocal()
        self.whatsapp_channel = WhatsappMessage()

    def check_client_alerts(self):
        appointments = repository.appointment.get_all_appointment_taken_and_notification_pending(self.db)
        print(appointments)
        for appointment in appointments:
            self.whatsapp_channel.send(appointment.client, "remember_date",
                                       [
                                           appointment.doctor_name, utils.format_date(appointment.appointment_date)])
            appointment.notified = True
            self.db.add(appointment)
            self.db.commit()
