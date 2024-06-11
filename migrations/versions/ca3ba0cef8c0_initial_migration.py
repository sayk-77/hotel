"""Initial migration

Revision ID: ca3ba0cef8c0
Revises: 
Create Date: 2024-05-28 17:45:36.189341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca3ba0cef8c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('position', sa.String(length=50), nullable=True),
    sa.Column('hire_date', sa.Date(), nullable=True),
    sa.Column('salary', sa.Numeric(), nullable=True),
    sa.Column('contact_info', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('guests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('contact_info', sa.String(length=100), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('id_document', sa.String(length=50), nullable=True),
    sa.Column('check_in_out_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hotelrooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_number', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('booking_number', sa.String(length=50), nullable=True),
    sa.Column('booking_date', sa.Date(), nullable=True),
    sa.Column('guest_id', sa.Integer(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['guest_id'], ['guests.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['hotelrooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employees_services',
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], ),
    sa.PrimaryKeyConstraint('employee_id', 'service_id')
    )
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transaction_id', sa.String(length=50), nullable=True),
    sa.Column('sale_date', sa.Date(), nullable=True),
    sa.Column('guest_id', sa.Integer(), nullable=True),
    sa.Column('sale_amount', sa.Numeric(), nullable=True),
    sa.Column('payment_method', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['guest_id'], ['guests.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sales')
    op.drop_table('employees_services')
    op.drop_table('bookings')
    op.drop_table('services')
    op.drop_table('hotelrooms')
    op.drop_table('guests')
    op.drop_table('employees')
    # ### end Alembic commands ###
