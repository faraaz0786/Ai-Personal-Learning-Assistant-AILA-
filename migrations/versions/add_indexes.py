"""add indexes

Revision ID: add_indexes
Revises: 
Create Date: 2026-03-24 01:15:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'add_indexes'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # sessions
    op.create_index('idx_sessions_created_at', 'sessions', ['created_at'])

    # topics
    op.create_index('idx_topics_session_id', 'topics', ['session_id'])
    op.create_index('idx_topics_normalized_topic', 'topics', ['normalized_topic'])

    # explanations
    op.create_index('idx_explanations_topic_id', 'explanations', ['topic_id'])
    op.create_index('idx_explanations_created_at', 'explanations', ['created_at'])

    # quizzes
    op.create_index('idx_quizzes_topic_id', 'quizzes', ['topic_id'])

    # quiz_attempts
    op.create_index('idx_quiz_attempts_session_id', 'quiz_attempts', ['session_id'])
    op.create_index('idx_quiz_attempts_quiz_id', 'quiz_attempts', ['quiz_id'])
    op.create_index('idx_quiz_attempts_attempted_at', 'quiz_attempts', ['attempted_at'])


def downgrade() -> None:
    op.drop_index('idx_quiz_attempts_attempted_at', table_name='quiz_attempts')
    op.drop_index('idx_quiz_attempts_quiz_id', table_name='quiz_attempts')
    op.drop_index('idx_quiz_attempts_session_id', table_name='quiz_attempts')

    op.drop_index('idx_quizzes_topic_id', table_name='quizzes')

    op.drop_index('idx_explanations_created_at', table_name='explanations')
    op.drop_index('idx_explanations_topic_id', table_name='explanations')

    op.drop_index('idx_topics_normalized_topic', table_name='topics')
    op.drop_index('idx_topics_session_id', table_name='topics')

    op.drop_index('idx_sessions_created_at', table_name='sessions')
