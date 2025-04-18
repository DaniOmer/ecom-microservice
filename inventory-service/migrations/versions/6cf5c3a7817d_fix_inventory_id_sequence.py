"""fix_inventory_id_sequence

Revision ID: 6cf5c3a7817d
Revises: 987445724df1
Create Date: 2025-04-18 16:41:01.217259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cf5c3a7817d'
down_revision: Union[str, None] = '987445724df1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create a sequence for the id column
    op.execute("CREATE SEQUENCE IF NOT EXISTS inventories_id_seq")
    
    # Set the id column to use the sequence
    op.execute("ALTER TABLE inventories ALTER COLUMN id SET DEFAULT nextval('inventories_id_seq')")
    
    # Set the sequence to be owned by the id column
    op.execute("ALTER SEQUENCE inventories_id_seq OWNED BY inventories.id")
    
    # Set the sequence to start from the current max id + 1
    op.execute("""
    SELECT setval('inventories_id_seq', COALESCE((SELECT MAX(id) FROM inventories), 0) + 1, false)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the default value from the id column
    op.execute("ALTER TABLE inventories ALTER COLUMN id DROP DEFAULT")
    
    # Drop the sequence
    op.execute("DROP SEQUENCE IF EXISTS inventories_id_seq")
