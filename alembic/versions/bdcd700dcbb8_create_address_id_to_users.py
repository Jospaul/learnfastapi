"""create address_id to users

Revision ID: bdcd700dcbb8
Revises: 57be6ea0495f
Create Date: 2023-03-09 11:22:31.755384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdcd700dcbb8'
down_revision = '57be6ea0495f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("address_id", sa.Integer(), nullable=True))
    op.create_foreign_key("address_user_fk", source_table="users", referent_table="address",
                          local_cols=["address_id"], remote_cols=["id"],ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("address_user_fk", table_name="users")
    op.drop_column("users","address_id")
