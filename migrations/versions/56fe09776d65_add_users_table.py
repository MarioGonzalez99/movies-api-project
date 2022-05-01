"""add users table

Revision ID: 56fe09776d65
Revises: 4bce19ff28c6
Create Date: 2022-02-19 16:23:05.109173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56fe09776d65'
down_revision = '4bce19ff28c6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('user_id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('username', sa.String(255),
                              unique=True, nullable=False),
                    sa.Column('password', sa.String(255), nullable=False),
                    sa.Column('rol_id', sa.Integer(), sa.ForeignKey(
                        "roles.rol_id"), nullable=False),
                    sa.Column('active', sa.Boolean(), nullable=False),
                    sa.Column('user_img', sa.String(255), nullable=True)
                    )

    pass


def downgrade():
    op.drop_table('users')
    pass
