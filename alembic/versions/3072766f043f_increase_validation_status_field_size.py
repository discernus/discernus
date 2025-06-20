"""increase_validation_status_field_size

Revision ID: 3072766f043f
Revises: 574edb17ee08
Create Date: 2025-06-19 22:34:51.406935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3072766f043f'
down_revision: Union[str, None] = '574edb17ee08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Increase validation_status field size from 20 to 50 characters."""
    
    # Increase validation_status in framework_versions table
    op.alter_column('framework_versions', 'validation_status',
               existing_type=sa.String(length=20),
               type_=sa.String(length=50),
               existing_nullable=True)
    
    # Increase validation_status in prompt_templates table  
    op.alter_column('prompt_templates', 'validation_status',
               existing_type=sa.String(length=20),
               type_=sa.String(length=50),
               existing_nullable=True)
    
    # Increase validation_status in weighting_methodologies table
    op.alter_column('weighting_methodologies', 'validation_status',
               existing_type=sa.String(length=20),
               type_=sa.String(length=50),
               existing_nullable=True)
    
    # Increase validation_status in component_compatibility table
    op.alter_column('component_compatibility', 'validation_status',
               existing_type=sa.String(length=20),
               type_=sa.String(length=50),
               existing_nullable=True)


def downgrade() -> None:
    """Revert validation_status field size back to 20 characters."""
    
    # Revert component_compatibility validation_status back to 20 characters
    op.alter_column('component_compatibility', 'validation_status',
               existing_type=sa.String(length=50),
               type_=sa.String(length=20),
               existing_nullable=True)
    
    # Revert weighting_methodologies validation_status back to 20 characters
    op.alter_column('weighting_methodologies', 'validation_status',
               existing_type=sa.String(length=50),
               type_=sa.String(length=20),
               existing_nullable=True)
    
    # Revert prompt_templates validation_status back to 20 characters
    op.alter_column('prompt_templates', 'validation_status',
               existing_type=sa.String(length=50),
               type_=sa.String(length=20),
               existing_nullable=True)
    
    # Revert framework_versions validation_status back to 20 characters
    op.alter_column('framework_versions', 'validation_status',
               existing_type=sa.String(length=50),
               type_=sa.String(length=20),
               existing_nullable=True)
