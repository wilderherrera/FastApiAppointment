"""create_initial_tables

Revision ID: 7587586d3945
Revises: 
Create Date: 2023-11-03 13:38:49.550900

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
# revision identifiers, used by Alembic.
from faker import Faker

revision: str = '7587586d3945'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100)),
        sa.Column('identification', sa.String(100)),
        sa.Column('identification_type', sa.String(100)),
        sa.Column('cellphone', sa.String(100)),
        sa.Column('date_of_birth', sa.Date),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('taken', sa.Boolean, default=False),
        sa.Column('notified', sa.Boolean, default=False),
        sa.Column('client_id', sa.Integer, sa.ForeignKey('clients.id'), nullable=False),
        sa.Column('appointment_date', sa.DateTime, nullable=False),
        sa.Column('doctor_name', sa.String(100), nullable=False),
        sa.Column('reason', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    # Inserta 100 clientes con datos aleatorios
    fake = Faker()
    conn = op.get_bind()

    for _ in range(100):
        identification_type = fake.random_element(elements=("CC", "TI"))

        conn.execute(
            sa.text(
                "INSERT INTO clients (first_name, last_name, email, identification, identification_type, cellphone, date_of_birth) "
                "VALUES (:first_name, :last_name, :email, :identification, :identification_type, :cellphone, :date_of_birth)"
            ),
            {
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "identification": fake.ssn(),
                "identification_type": identification_type,  # Usar el valor aleatorio
                "cellphone": fake.phone_number(),
                "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=90),
            }
        )

    # Agrega la restricción de verificación (CHECK constraint)
    op.create_check_constraint(
        "check_identification_type",
        "clients",
        sa.or_(
            sa.text("identification_type = 'CC'"),
            sa.text("identification_type = 'TI'")
        )
    )


# Define la tabla "dates"
def downgrade():
    op.drop_table('clients')
    op.drop_table('appointments')
