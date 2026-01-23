"""empty message

Revision ID: 7d8017efcec7
Revises: 7736cdd5af82
Create Date: 2026-01-03 09:47:48.546497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d8017efcec7'
down_revision: Union[str, Sequence[str], None] = '7736cdd5af82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
