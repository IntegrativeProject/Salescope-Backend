"""init

Revision ID: 38ef320006c6
Revises: 7a63eea012d6
Create Date: 2025-11-24 23:25:22.742656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38ef320006c6'
down_revision: Union[str, Sequence[str], None] = '7a63eea012d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
