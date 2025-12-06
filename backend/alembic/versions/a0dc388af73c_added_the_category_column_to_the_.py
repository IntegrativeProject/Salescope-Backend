"""add_category_to_products

Revision ID: [new_revision_id]
Revises: [previous_revision_id]
Create Date: 2025-12-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '[new_revision_id]'
down_revision = '[previous_revision_id]'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        'products',
        sa.Column('category', sa.String(length=100), nullable=True, comment='Category of the product')
    )

def downgrade():
    op.drop_column('products', 'category')