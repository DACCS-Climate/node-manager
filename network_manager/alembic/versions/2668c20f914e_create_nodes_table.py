"""create nodes table

Revision ID: 2668c20f914e
Revises:
Create Date: 2023-04-04 15:48:46.205580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2668c20f914e"
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
        sa.Column("support_contact_email", sa.String(50)),
        sa.Column("deploy_start_date", sa.Date),
        sa.Column("data", sa.Boolean(), nullable=True),
        sa.Column("compute", sa.Boolean(), nullable=True),
        sa.Column("administrator", sa.String(100), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("nodes")
