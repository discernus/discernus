"""Add experiment and run tables for v2.1

Revision ID: 6bd6192013ca
Revises: f6587a1dad12
Create Date: 2025-01-06 20:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6bd6192013ca'
down_revision = 'f6587a1dad12'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create experiment table
    op.create_table('experiment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('hypothesis', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('research_context', sa.Text(), nullable=True),
    sa.Column('prompt_template_id', sa.String(length=100), nullable=False),
    sa.Column('framework_config_id', sa.String(length=100), nullable=False),
    sa.Column('scoring_algorithm_id', sa.String(length=100), nullable=False),
    sa.Column('analysis_mode', sa.String(length=50), nullable=True),
    sa.Column('selected_models', sa.JSON(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('total_runs', sa.Integer(), nullable=True),
    sa.Column('successful_runs', sa.Integer(), nullable=True),
    sa.Column('research_notes', sa.Text(), nullable=True),
    sa.Column('publication_status', sa.String(length=50), nullable=True),
    sa.Column('tags', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_experiment_id'), 'experiment', ['id'], unique=False)

    # Create run table
    op.create_table('run',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('experiment_id', sa.Integer(), nullable=False),
    sa.Column('run_number', sa.Integer(), nullable=False),
    sa.Column('text_id', sa.String(length=255), nullable=True),
    sa.Column('text_content', sa.Text(), nullable=False),
    sa.Column('input_length', sa.Integer(), nullable=False),
    sa.Column('llm_model', sa.String(length=100), nullable=False),
    sa.Column('llm_version', sa.String(length=50), nullable=True),
    sa.Column('prompt_template_version', sa.String(length=20), nullable=False),
    sa.Column('framework_version', sa.String(length=20), nullable=False),
    sa.Column('raw_scores', sa.JSON(), nullable=False),
    sa.Column('hierarchical_ranking', sa.JSON(), nullable=True),
    sa.Column('framework_fit_score', sa.Float(), nullable=True),
    sa.Column('well_justifications', sa.JSON(), nullable=True),
    sa.Column('narrative_elevation', sa.Float(), nullable=True),
    sa.Column('polarity', sa.Float(), nullable=True),
    sa.Column('coherence', sa.Float(), nullable=True),
    sa.Column('directional_purity', sa.Float(), nullable=True),
    sa.Column('narrative_position_x', sa.Float(), nullable=True),
    sa.Column('narrative_position_y', sa.Float(), nullable=True),
    sa.Column('execution_time', sa.DateTime(), nullable=True),
    sa.Column('duration_seconds', sa.Float(), nullable=True),
    sa.Column('api_cost', sa.Float(), nullable=True),
    sa.Column('raw_prompt', sa.Text(), nullable=True),
    sa.Column('raw_response', sa.Text(), nullable=True),
    sa.Column('model_parameters', sa.JSON(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('success', sa.Boolean(), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('complete_provenance', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['experiment_id'], ['experiment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_run_id'), 'run', ['id'], unique=False)

    # Add experiment_id column to existing job table
    op.add_column('job', sa.Column('experiment_id', sa.Integer(), nullable=True))
    op.add_column('job', sa.Column('prompt_template_config', sa.JSON(), nullable=True))
    op.add_column('job', sa.Column('scoring_algorithm', sa.String(length=50), nullable=True))
    op.add_column('job', sa.Column('analysis_mode', sa.String(length=50), nullable=True))
    op.create_foreign_key('fk_job_experiment', 'job', 'experiment', ['experiment_id'], ['id'])

    # Add enhanced columns to existing task table
    op.add_column('task', sa.Column('hierarchical_result', sa.JSON(), nullable=True))
    op.add_column('task', sa.Column('justifications', sa.JSON(), nullable=True))


def downgrade() -> None:
    # Remove added columns from task table
    op.drop_column('task', 'justifications')
    op.drop_column('task', 'hierarchical_result')
    
    # Remove added columns from job table
    op.drop_constraint('fk_job_experiment', 'job', type_='foreignkey')
    op.drop_column('job', 'analysis_mode')
    op.drop_column('job', 'scoring_algorithm')
    op.drop_column('job', 'prompt_template_config')
    op.drop_column('job', 'experiment_id')
    
    # Drop new tables
    op.drop_index(op.f('ix_run_id'), table_name='run')
    op.drop_table('run')
    op.drop_index(op.f('ix_experiment_id'), table_name='experiment')
    op.drop_table('experiment')
