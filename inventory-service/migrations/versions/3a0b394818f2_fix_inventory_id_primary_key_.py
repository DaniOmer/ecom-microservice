"""fix_inventory_id_primary_key_autoincrement

Revision ID: 3a0b394818f2
Revises: bca4e03b1dee
Create Date: 2025-04-18 16:39:05.075202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a0b394818f2'
down_revision: Union[str, None] = 'bca4e03b1dee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_inventories_id'), 'inventories', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_inventories_id'), table_name='inventories')
    # ### end Alembic commands ###
