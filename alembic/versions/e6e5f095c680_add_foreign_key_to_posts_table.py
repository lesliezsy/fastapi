"""add foreign-key to posts table

Revision ID: e6e5f095c680
Revises: 255b84893e1d
Create Date: 2025-04-25 02:25:01.495913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6e5f095c680'
down_revision: Union[str, None] = '255b84893e1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # op.add_column('posts', sa.Column('owner_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False))
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table = 'posts', referent_table= 'users', local_cols= ['owner_id'], remote_cols= ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
