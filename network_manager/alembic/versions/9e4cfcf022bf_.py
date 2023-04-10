"""Merged previous heads
   Added boolean columns
   Dropped capabilities field

Revision ID: 9e4cfcf022bf
Revises: 2668c20f914e, 621a290666b8
Create Date: 2023-04-10 11:05:28.900662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9e4cfcf022bf"
down_revision = ("2668c20f914e", "621a290666b8")
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("nodes", "capabilities")
    op.add_column("nodes", sa.Column("weaver", sa.Boolean(), nullable=True)),
    op.add_column("nodes", sa.Column("catalog", sa.Boolean(), nullable=True)),
    op.add_column("nodes", sa.Column("jupyter", sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.add_column("nodes", sa.Column("capabilities", sa.String(200))),
    op.drop_column("nodes", "weaver"),
    op.drop_column("nodes", "catalog"),
    op.drop_column("nodes", "jupyter")
