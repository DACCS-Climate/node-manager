"""create nodes table

Revision ID: 621a290666b8
Revises: 2668c20f914e
Create Date: 2023-04-05 16:05:39.918614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "621a290666b8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "nodes",
        sa.Column("node_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("node_name", sa.String(50), nullable=False),
        sa.Column("node_description", sa.String(200)),
        sa.Column("location", sa.String(50)),
        sa.Column("affiliation", sa.String(50)),
        sa.Column("url", sa.String(50)),
        sa.Column("capabilities", sa.String(200)),
        sa.Column("user_email", sa.String(50)),
        sa.Column("deploy_start_date", sa.Date),
    )


def downgrade() -> None:
    op.drop_table("nodes")
