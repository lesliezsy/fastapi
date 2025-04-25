"""add user table

Revision ID: 255b84893e1d
Revises: a3e6864a67bb
Create Date: 2025-04-25 02:15:17.415914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '255b84893e1d'
down_revision: Union[str, None] = 'a3e6864a67bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'))
                 
    pass



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
