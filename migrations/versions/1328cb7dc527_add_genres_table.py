"""add genres table

Revision ID: 1328cb7dc527
Revises: 56fe09776d65
Create Date: 2022-02-19 16:54:52.105723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1328cb7dc527'
down_revision = '56fe09776d65'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('genres',
                    sa.Column('genre_id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('name', sa.String(100),
                              unique=True, nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('roles')
    pass
