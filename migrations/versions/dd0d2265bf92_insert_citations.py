"""insert_citations

Revision ID: dd0d2265bf92
Revises: 7587586d3945
Create Date: 2023-11-03 13:46:48.104929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from faker.providers.person.es_MX import Provider as PersonProvider

# revision identifiers, used by Alembic.
from faker import Faker

revision: str = 'dd0d2265bf92'
down_revision: Union[str, None] = '7587586d3945'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Utiliza Faker en español con nombres latinos
    fake = Faker('es_MX')
    fake.add_provider(PersonProvider)

    conn = op.get_bind()

    for client_id in range(1, 6):  # IDs de cliente del 1 al 5
        for _ in range(10):  # Inserta 10 citas por cliente
            appointment_date = fake.date_time_this_decade()
            doctor_name = fake.first_name() + ' ' + fake.last_name()
            reason = fake.sentence(nb_words=10, variable_nb_words=True,
                                   ext_word_list=None)  # Genera una razón médica de hasta 10 palabras

            conn.execute(
                sa.text(
                    "INSERT INTO appointments (client_id, appointment_date, doctor_name, reason, created_at,taken) "
                    "VALUES (:client_id, :appointment_date, :doctor_name, :reason, NOW(),FALSE)"
                ),
                {
                    "client_id": client_id,
                    "appointment_date": appointment_date,
                    "doctor_name": doctor_name,
                    "reason": reason,
                }
            )


def downgrade() -> None:
    pass
