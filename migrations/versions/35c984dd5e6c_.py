"""empty message

Revision ID: 35c984dd5e6c
Revises: e3532d24a41b
Create Date: 2020-10-06 16:07:38.072287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35c984dd5e6c'
down_revision = 'e3532d24a41b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('address', 'brei')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('brei', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
