"""empty message

Revision ID: 2c579199005
Revises: 1f9c61031fa
Create Date: 2016-01-26 17:21:29.659591

"""

# revision identifiers, used by Alembic.
revision = '2c579199005'
down_revision = '1f9c61031fa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.String(length=255), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'name')
    ### end Alembic commands ###
