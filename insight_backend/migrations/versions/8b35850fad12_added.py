"""added

Revision ID: 8b35850fad12
Revises: 959be8a8e56c
Create Date: 2024-01-02 23:03:13.560605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b35850fad12'
down_revision: Union[str, None] = '959be8a8e56c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pending_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_repr', sa.String(length=100), nullable=False),
    sa.Column('is_username_repr', sa.Boolean(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'creator', 'client', name='userroles'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_repr')
    )
    op.add_column('users', sa.Column('telegram_repr', sa.String(length=100), nullable=False))
    op.add_column('users', sa.Column('is_username_repr', sa.Boolean(), nullable=False))
    op.create_unique_constraint(None, 'users', ['telegram_repr'])
    op.drop_column('users', 'is_username_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_username_id', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'is_username_repr')
    op.drop_column('users', 'telegram_repr')
    op.drop_table('pending_users')
    # ### end Alembic commands ###
