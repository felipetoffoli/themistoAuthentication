"""empty message

Revision ID: be7035c16fa3
Revises: b64a8fd4ef4d
Create Date: 2020-07-13 22:56:24.682722

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'be7035c16fa3'
down_revision = 'b64a8fd4ef4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person_address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person_address',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('address_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('person_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('creation_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('modification_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], name='person_address_address_id_fkey'),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], name='person_address_person_id_fkey'),
    sa.PrimaryKeyConstraint('id', 'address_id', 'person_id', name='person_address_pkey')
    )
    # ### end Alembic commands ###