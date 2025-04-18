"""fix_inventory_primary_key_constraint

Revision ID: 987445724df1
Revises: 3a0b394818f2
Create Date: 2025-04-18 16:39:12.963097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '987445724df1'
down_revision: Union[str, None] = '3a0b394818f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the existing primary key constraint on product_uid
    op.drop_constraint('inventories_pkey', 'inventories', type_='primary')
    
    # Make id column primary key with autoincrement
    op.alter_column('inventories', 'id', 
                    existing_type=sa.Integer(), 
                    nullable=False,
                    autoincrement=True)
    op.create_primary_key('inventories_pkey', 'inventories', ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Revert back to product_uid as primary key
    op.drop_constraint('inventories_pkey', 'inventories', type_='primary')
    op.create_primary_key('inventories_pkey', 'inventories', ['product_uid'])
