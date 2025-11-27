"""Ensuring the functionality of the delete_at and delete_by in user and product model

Revision ID: 568a79361617
Revises: 2f460ff9c3e4
Create Date: 2025-11-27 09:35:07.640441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '568a79361617'
down_revision: Union[str, Sequence[str], None] = '2f460ff9c3e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
