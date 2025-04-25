"""add content column to posts table

Revision ID: a3e6864a67bb
Revises: cce62cb0e68e
Create Date: 2025-04-25 02:05:43.701979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3e6864a67bb'
down_revision: Union[str, None] = 'cce62cb0e68e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
