"""empty message

Revision ID: 7736cdd5af82
Revises: dca080868dfe
Create Date: 2026-01-03 09:47:08.573642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7736cdd5af82'
down_revision: Union[str, Sequence[str], None] = 'dca080868dfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
