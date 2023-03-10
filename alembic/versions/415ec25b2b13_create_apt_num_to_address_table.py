"""create apt_num to address table

Revision ID: 415ec25b2b13
Revises: bdcd700dcbb8
Create Date: 2023-03-09 11:58:17.075682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '415ec25b2b13'
down_revision = 'bdcd700dcbb8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("address", sa.Column("apt_num", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("address","apt_num")
