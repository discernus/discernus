"""Increase varchar limits for framework_version and prompt_template_version

Revision ID: increase_varchar_limits_20250610
Revises: f6587a1dad12
Create Date: 2025-06-10 10:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'increase_varchar_limits_20250610'
down_revision: Union[str, None] = 'f6587a1dad12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Increase varchar limits for version fields."""
    # Increase prompt_template_version from 20 to 50 characters
    op.alter_column('run', 'prompt_template_version',
               existing_type=sa.String(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)
    
    # Increase framework_version from 20 to 50 characters  
    op.alter_column('run', 'framework_version',
               existing_type=sa.String(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)


def downgrade() -> None:
    """Revert varchar limits back to 20 characters."""
    # Revert framework_version back to 20 characters
    op.alter_column('run', 'framework_version',
               existing_type=sa.String(length=50),
               type_=sa.String(length=20),
               existing_nullable=False)
    
    # Revert prompt_template_version back to 20 characters
    op.alter_column('run', 'prompt_template_version',
               existing_type=sa.String(length=50),
               type_=sa.String(length=20),
               existing_nullable=False) 