"""Add per to indicate price for floor/sqm/building

Revision ID: 962848c31228
Revises: 2eb825d9e46e
Create Date: 2022-08-11 12:06:27.574238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '962848c31228'
down_revision = '2eb825d9e46e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prices', sa.Column('per', sa.Enum('building', 'sqm', 'floor', name='priceby'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('prices', 'per')
    # ### end Alembic commands ###
