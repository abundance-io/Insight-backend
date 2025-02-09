"""drop

Revision ID: e2476ada594b
Revises: 66cc0c791c96
Create Date: 2023-12-19 13:06:24.083692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2476ada594b'
down_revision: Union[str, None] = '66cc0c791c96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('passkey', sa.VARCHAR(length=228), autoincrement=False, nullable=False),
    sa.Column('telegram_id', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('is_username_id', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('role', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('telegram_id', name='users_telegram_id_key')
    )
    # ### end Alembic commands ###
