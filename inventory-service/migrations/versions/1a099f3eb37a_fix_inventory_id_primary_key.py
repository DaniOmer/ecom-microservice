"""fix_inventory_id_primary_key

Revision ID: 1a099f3eb37a
Revises: f405efd0a96f
Create Date: 2025-04-18 16:32:35.870749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a099f3eb37a'
down_revision: Union[str, None] = 'f405efd0a96f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
