"""empty message

Revision ID: 3ecc9b116c2
Revises: 213a2b3c099
Create Date: 2015-12-15 16:44:31.661766

"""

# revision identifiers, used by Alembic.
revision = '3ecc9b116c2'
down_revision = '213a2b3c099'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags_posts',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.drop_column('post', 'tags')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('tags', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_table('tags_posts')
    op.drop_table('tag')
    ### end Alembic commands ###
