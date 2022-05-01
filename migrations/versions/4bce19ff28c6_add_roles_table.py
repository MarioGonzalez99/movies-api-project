"""add roles table

Revision ID: 4bce19ff28c6
Revises: 
Create Date: 2022-02-18 20:53:27.910746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bce19ff28c6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('roles',
                    sa.Column('rol_id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('name', sa.String(100),
                              unique=True, nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('roles')
    pass
