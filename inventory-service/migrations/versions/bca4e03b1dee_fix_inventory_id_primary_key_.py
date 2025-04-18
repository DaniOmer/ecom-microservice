"""fix_inventory_id_primary_key_

Revision ID: bca4e03b1dee
Revises: 1a099f3eb37a
Create Date: 2025-04-18 16:34:55.136682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bca4e03b1dee'
down_revision: Union[str, None] = '1a099f3eb37a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
