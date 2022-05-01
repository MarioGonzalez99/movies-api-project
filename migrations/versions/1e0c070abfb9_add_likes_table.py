"""add likes table

Revision ID: 1e0c070abfb9
Revises: 6dbafcb258bf
Create Date: 2022-02-19 17:37:05.217694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e0c070abfb9'
down_revision = '6dbafcb258bf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('movies_likes',
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey(
                        'users.user_id', ondelete='CASCADE'), primary_key=True),
                    sa.Column('movie_id', sa.Integer(), sa.ForeignKey(
                        'movies.movie_id', ondelete='CASCADE'), primary_key=True)
                    )
    pass


def downgrade():
    op.drop_table('movies_likes')
    pass
