"""add server default for photo updated_at

Revision ID: 1bf2566ebc02
Revises: 377965c51823
Create Date: 2026-01-21 21:08:49.271391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bf2566ebc02'
down_revision: Union[str, Sequence[str], None] = '377965c51823'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # updated_at: adicionar server_default
    op.alter_column(
        'photos',
        'updated_at',
        existing_type=sa.TIMESTAMP(timezone=True),
        server_default=sa.text('NOW()'),
        existing_nullable=True  # porque já tem onupdate no SQLAlchemy
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'photos',
        'updated_at',
        existing_type=sa.TIMESTAMP(timezone=True),
        server_default=None,
        existing_nullable=True
    )
