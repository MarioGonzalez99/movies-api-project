"""add movies table

Revision ID: 6dbafcb258bf
Revises: 1328cb7dc527
Create Date: 2022-02-19 16:56:13.126216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dbafcb258bf'
down_revision = '1328cb7dc527'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('movies',
                    sa.Column('movie_id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('title', sa.String(100),
                              unique=True, nullable=False),
                    sa.Column('description', sa.String(1000), nullable=True),
                    sa.Column('date_released', sa.Date(), nullable=False),
                    sa.Column('genre_id', sa.Integer(), sa.ForeignKey(
                        "genres.genre_id"), nullable=False),
                    sa.Column('budget', sa.Integer(), nullable=False),
                    sa.Column('revenue', sa.Integer(), nullable=False),
                    sa.Column('movie_img', sa.String(255), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('movies')
    pass
