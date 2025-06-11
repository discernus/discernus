"""update_experiment_foreign_keys_and_populate_components

Revision ID: 574edb17ee08
Revises: 21321e96db52
Create Date: 2025-06-11 17:40:55.264809

"""
from typing import Sequence, Union
import uuid
import json
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '574edb17ee08'
down_revision: Union[str, None] = '21321e96db52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema with component versioning support."""
    
    # Get connection for data operations
    conn = op.get_bind()
    
    # First, populate component versioning tables with existing framework data
    populate_component_tables(conn)
    
    # Add new foreign key columns to experiment table
    op.add_column('experiment', sa.Column('prompt_template_version_id', sa.String(36), nullable=True))
    op.add_column('experiment', sa.Column('framework_version_id', sa.String(36), nullable=True))
    op.add_column('experiment', sa.Column('weighting_method_version_id', sa.String(36), nullable=True))
    
    # Migrate existing experiment data to use foreign keys
    migrate_experiment_data(conn)
    
    # Add foreign key constraints
    op.create_foreign_key('fk_experiment_prompt_template', 'experiment', 'prompt_templates', 
                         ['prompt_template_version_id'], ['id'])
    op.create_foreign_key('fk_experiment_framework', 'experiment', 'framework_versions', 
                         ['framework_version_id'], ['id'])
    op.create_foreign_key('fk_experiment_weighting', 'experiment', 'weighting_methodologies', 
                         ['weighting_method_version_id'], ['id'])
    
    # Update run table to use foreign keys for component versioning
    op.add_column('run', sa.Column('prompt_template_version_id', sa.String(36), nullable=True))
    op.add_column('run', sa.Column('framework_version_id', sa.String(36), nullable=True))
    op.add_column('run', sa.Column('weighting_method_version_id', sa.String(36), nullable=True))
    
    # Migrate existing run data
    migrate_run_data(conn)
    
    # Add foreign key constraints for run table
    op.create_foreign_key('fk_run_prompt_template', 'run', 'prompt_templates', 
                         ['prompt_template_version_id'], ['id'])
    op.create_foreign_key('fk_run_framework', 'run', 'framework_versions', 
                         ['framework_version_id'], ['id'])
    op.create_foreign_key('fk_run_weighting', 'run', 'weighting_methodologies', 
                         ['weighting_method_version_id'], ['id'])


def populate_component_tables(conn):
    """Populate component versioning tables with current framework data."""
    
    # 1. Populate prompt_templates table
    default_prompt_id = str(uuid.uuid4())
    conn.execute(
        sa.text("""
            INSERT INTO prompt_templates (id, name, version, template_content, description, created_by, created_at)
            VALUES (:id, :name, :version, :content, :desc, :creator, :created)
        """),
        {
            'id': default_prompt_id,
            'name': 'civic_virtue_hierarchical',
            'version': '2.1.0',
            'content': '''Analyze the following text for its narrative positioning within civic virtue frameworks.

Consider the hierarchical relationship between wells:
- Primary wells (40-50% influence): Dominant narrative themes
- Secondary wells (30-35% influence): Supporting narrative elements  
- Tertiary wells (15-25% influence): Background narrative presence

TEXT TO ANALYZE:
{text_content}

Provide scores (0.0-1.0) for each civic virtue well and explain the hierarchical relationships.''',
            'desc': 'Default hierarchical prompt template for civic virtue analysis',
            'creator': None,  # NULL for system migration
            'created': datetime.utcnow()
        }
    )
    
    # 2. Populate framework_versions table with civic virtue framework
    framework_id = str(uuid.uuid4())
    civic_virtue_config = {
        "wells": {
            "constructive": ["Dignity", "Truth", "Justice", "Hope", "Pragmatism"],
            "destructive": ["Tribalism", "Manipulation", "Resentment", "Fantasy", "Fear"]
        },
        "dipoles": [
            {"positive": "Dignity", "negative": "Tribalism", "axis": "Community"},
            {"positive": "Truth", "negative": "Manipulation", "axis": "Information"},
            {"positive": "Justice", "negative": "Resentment", "axis": "Fairness"},
            {"positive": "Hope", "negative": "Fantasy", "axis": "Future"},
            {"positive": "Pragmatism", "negative": "Fear", "axis": "Action"}
        ],
        "scoring": {
            "method": "hierarchical_weighted",
            "primary_weight": 0.45,
            "secondary_weight": 0.35,
            "tertiary_weight": 0.20
        }
    }
    
    conn.execute(
        sa.text("""
            INSERT INTO framework_versions (id, framework_name, version, dipoles_json, framework_json, weights_json, description, created_by, created_at)
            VALUES (:id, :name, :version, :dipoles, :framework, :weights, :desc, :creator, :created)
        """),
        {
            'id': framework_id,
            'name': 'civic_virtue',
            'version': '2.1.0',
            'dipoles': json.dumps(civic_virtue_config['dipoles']),
            'framework': json.dumps(civic_virtue_config),
            'weights': json.dumps(civic_virtue_config['scoring']),
            'desc': 'Civic virtue framework with hierarchical scoring support',
            'creator': None,  # NULL for system migration
            'created': datetime.utcnow()
        }
    )
    
    # 3. Populate weighting_methodologies table
    weighting_id = str(uuid.uuid4())
    conn.execute(
        sa.text("""
            INSERT INTO weighting_methodologies (id, name, version, algorithm_description, mathematical_formula, implementation_notes, algorithm_type, parameters_json, created_by, created_at)
            VALUES (:id, :name, :version, :desc, :formula, :notes, :algorithm_type, :parameters, :creator, :created)
        """),
        {
            'id': weighting_id,
            'name': 'hierarchical_weighted',
            'version': '2.1.0',
            'desc': 'Hierarchical weighting algorithm that assigns primary (45%), secondary (35%), and tertiary (20%) weights to wells based on prominence',
            'formula': 'final_score = Σ(well_score * hierarchy_weight) where hierarchy_weight ∈ {0.45, 0.35, 0.20}',
            'notes': 'Wells are ranked by raw LLM scores, then assigned to hierarchy tiers. Final narrative position calculated using weighted averages.',
            'algorithm_type': 'hierarchical_weighted',
            'parameters': json.dumps({
                'primary_weight': 0.45,
                'secondary_weight': 0.35,
                'tertiary_weight': 0.20,
                'tier_assignment': 'score_ranked'
            }),
            'creator': None,  # NULL for system migration
            'created': datetime.utcnow()
        }
    )
    
    # Store IDs for migration use
    conn.execute(
        sa.text("""
            CREATE TEMPORARY TABLE temp_component_ids (
                component_type VARCHAR(50),
                component_id VARCHAR(36)
            )
        """)
    )
    
    conn.execute(
        sa.text("""
            INSERT INTO temp_component_ids VALUES 
            ('prompt_template', :prompt_id),
            ('framework', :framework_id),
            ('weighting', :weighting_id)
        """),
        {
            'prompt_id': default_prompt_id,
            'framework_id': framework_id,
            'weighting_id': weighting_id
        }
    )


def migrate_experiment_data(conn):
    """Migrate existing experiment data to use component versioning foreign keys."""
    
    # Get component IDs from temp table
    result = conn.execute(sa.text("SELECT component_type, component_id FROM temp_component_ids"))
    components = {row[0]: row[1] for row in result}
    
    # Update all existing experiments to use the new foreign keys
    conn.execute(
        sa.text("""
            UPDATE experiment SET 
                prompt_template_version_id = :prompt_id,
                framework_version_id = :framework_id,
                weighting_method_version_id = :weighting_id
            WHERE prompt_template_version_id IS NULL
        """),
        {
            'prompt_id': components['prompt_template'],
            'framework_id': components['framework'],
            'weighting_id': components['weighting']
        }
    )


def migrate_run_data(conn):
    """Migrate existing run data to use component versioning foreign keys."""
    
    # Get component IDs from temp table
    result = conn.execute(sa.text("SELECT component_type, component_id FROM temp_component_ids"))
    components = {row[0]: row[1] for row in result}
    
    # Update all existing runs to use the new foreign keys
    conn.execute(
        sa.text("""
            UPDATE run SET 
                prompt_template_version_id = :prompt_id,
                framework_version_id = :framework_id,
                weighting_method_version_id = :weighting_id
            WHERE prompt_template_version_id IS NULL
        """),
        {
            'prompt_id': components['prompt_template'],
            'framework_id': components['framework'],
            'weighting_id': components['weighting']
        }
    )


def downgrade() -> None:
    """Downgrade schema - remove component versioning foreign keys."""
    
    # Drop foreign key constraints from run table
    op.drop_constraint('fk_run_weighting', 'run', type_='foreignkey')
    op.drop_constraint('fk_run_framework', 'run', type_='foreignkey')
    op.drop_constraint('fk_run_prompt_template', 'run', type_='foreignkey')
    
    # Drop columns from run table
    op.drop_column('run', 'weighting_method_version_id')
    op.drop_column('run', 'framework_version_id')
    op.drop_column('run', 'prompt_template_version_id')
    
    # Drop foreign key constraints from experiment table
    op.drop_constraint('fk_experiment_weighting', 'experiment', type_='foreignkey')
    op.drop_constraint('fk_experiment_framework', 'experiment', type_='foreignkey')
    op.drop_constraint('fk_experiment_prompt_template', 'experiment', type_='foreignkey')
    
    # Drop columns from experiment table
    op.drop_column('experiment', 'weighting_method_version_id')
    op.drop_column('experiment', 'framework_version_id')
    op.drop_column('experiment', 'prompt_template_version_id')
