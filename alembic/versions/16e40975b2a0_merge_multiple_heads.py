"""merge_multiple_heads

Revision ID: 16e40975b2a0
Revises: 6bd6192013ca, increase_varchar_limits_20250610
Create Date: 2025-06-11 12:41:03.296962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16e40975b2a0'
down_revision: Union[str, None] = ('6bd6192013ca', 'increase_varchar_limits_20250610')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
