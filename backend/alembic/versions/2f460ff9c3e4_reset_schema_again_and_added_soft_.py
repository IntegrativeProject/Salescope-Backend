"""Reset schema again and added soft delete in users and products

Revision ID: 2f460ff9c3e4
Revises: 616b4c4f65e2
Create Date: 2025-11-27 09:02:30.153032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f460ff9c3e4'
down_revision: Union[str, Sequence[str], None] = '616b4c4f65e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
