"""added

Revision ID: dd346cc34add
Revises: 472356b22aca
Create Date: 2024-01-05 09:22:03.894164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd346cc34add'
down_revision: Union[str, None] = '472356b22aca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('creators',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='fk_creators_users_id_user'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coursedbs_creatorsdbs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creatorsdb', sa.Integer(), nullable=True),
    sa.Column('coursedb', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['coursedb'], ['courses.course_code'], name='fk_coursedbs_creatorsdbs_courses_coursedb_course_code', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['creatorsdb'], ['creators.id'], name='fk_coursedbs_creatorsdbs_creators_creatorsdb_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('coursedbs_creatorsdbs')
    op.drop_table('creators')
    # ### end Alembic commands ###
