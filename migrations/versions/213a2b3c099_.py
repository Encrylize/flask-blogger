"""empty message

Revision ID: 213a2b3c099
Revises: None
Create Date: 2015-12-14 18:40:53.379821

"""

# revision identifiers, used by Alembic.
revision = '213a2b3c099'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('body', sa.String(length=10000), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    ### end Alembic commands ###
