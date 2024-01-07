"""rearranged

Revision ID: 472356b22aca
Revises: bc60f697fc7f
Create Date: 2024-01-05 08:47:04.013903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '472356b22aca'
down_revision: Union[str, None] = 'bc60f697fc7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content', sa.Column('section', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_content_departments_id_section', 'content', 'departments', ['section'], ['id'])
    op.add_column('questions', sa.Column('quiz', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_questions_quizzes_id_quiz', 'questions', 'quizzes', ['quiz'], ['id'])
    op.drop_constraint('fk_sections_content_id_content', 'sections', type_='foreignkey')
    op.drop_column('sections', 'content')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sections', sa.Column('content', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_sections_content_id_content', 'sections', 'content', ['content'], ['id'])
    op.drop_constraint('fk_questions_quizzes_id_quiz', 'questions', type_='foreignkey')
    op.drop_column('questions', 'quiz')
    op.drop_constraint('fk_content_departments_id_section', 'content', type_='foreignkey')
    op.drop_column('content', 'section')
    # ### end Alembic commands ###
