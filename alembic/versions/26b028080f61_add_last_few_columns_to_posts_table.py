"""add last few columns to posts table

Revision ID: 26b028080f61
Revises: e6e5f095c680
Create Date: 2025-04-25 02:40:09.726216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26b028080f61'
down_revision: Union[str, None] = 'e6e5f095c680'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', 
                    sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False))
    op.add_column('posts', 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
