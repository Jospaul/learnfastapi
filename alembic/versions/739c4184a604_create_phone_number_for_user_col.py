"""Create phone number for user col

Revision ID: 739c4184a604
Revises: 
Create Date: 2023-03-09 10:48:35.631235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '739c4184a604'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
