"""Add fields to user table

Revision ID: a405a7f19525
Revises: d1277f33006f
Create Date: 2024-12-03 05:39:14.748429

"""

from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a405a7f19525"
down_revision: Union[str, None] = "d1277f33006f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("is_verified", sa.Boolean(), nullable=False))
    op.add_column("user", sa.Column("is_locked", sa.Boolean(), nullable=False))
    op.add_column("user", sa.Column("created_at", sa.DateTime(), nullable=False))
    op.add_column("user", sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.drop_column("user", "is_active")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    op.drop_column("user", "updated_at")
    op.drop_column("user", "created_at")
    op.drop_column("user", "is_locked")
    op.drop_column("user", "is_verified")
    # ### end Alembic commands ###