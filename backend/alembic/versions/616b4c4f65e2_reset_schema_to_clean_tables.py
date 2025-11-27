"""reset schema to clean tables

Revision ID: 616b4c4f65e2
Revises: be32ca3189cd
Create Date: 2025-11-26 22:09:42.391775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '616b4c4f65e2'
down_revision: Union[str, Sequence[str], None] = 'be32ca3189cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
