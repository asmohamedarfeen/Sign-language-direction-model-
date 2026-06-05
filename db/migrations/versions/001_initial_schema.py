"""Initial Schema Migration

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-11-03 15:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. vocabulary_signs
    op.create_table(
        'vocabulary_signs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('symbol', sa.String(length=32), nullable=False),
        sa.Column('label', sa.String(length=64), nullable=False),
        sa.Column('category', sa.String(length=32), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tips', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=256), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_vocabulary_signs_id', 'vocabulary_signs', ['id'], unique=False)
    op.create_index('ix_vocabulary_signs_symbol', 'vocabulary_signs', ['symbol'], unique=True)
    op.create_index('ix_vocabulary_signs_category', 'vocabulary_signs', ['category'], unique=False)

    # 2. recognition_logs
    op.create_table(
        'recognition_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.String(length=64), nullable=True),
        sa.Column('predicted_sign', sa.String(length=32), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('latency_ms', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_recognition_logs_id', 'recognition_logs', ['id'], unique=False)
    op.create_index('ix_recognition_logs_session_id', 'recognition_logs', ['session_id'], unique=False)
    op.create_index('ix_recognition_logs_predicted_sign', 'recognition_logs', ['predicted_sign'], unique=False)

    # 3. translation_sessions
    op.create_table(
        'translation_sessions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.String(length=64), nullable=False),
        sa.Column('translated_text', sa.Text(), nullable=False),
        sa.Column('total_gestures', sa.Integer(), nullable=False),
        sa.Column('avg_confidence', sa.Float(), nullable=False),
        sa.Column('duration_seconds', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_translation_sessions_id', 'translation_sessions', ['id'], unique=False)
    op.create_index('ix_translation_sessions_session_id', 'translation_sessions', ['session_id'], unique=False)


def downgrade() -> None:
    op.drop_table('translation_sessions')
    op.drop_table('recognition_logs')
    op.drop_table('vocabulary_signs')
