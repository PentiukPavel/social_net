"""empty message

Revision ID: 5fff92a336a0
Revises: e290c373276a
Create Date: 2024-10-30 16:00:42.453118

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5fff92a336a0"
down_revision: Union[str, None] = "e290c373276a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "favorites",
        sa.Column("favorite_id", sa.Integer(), nullable=False),
        sa.Column("subscriber_id", sa.Integer(), nullable=False),
        sa.Column("registered_at", sa.TIMESTAMP(), nullable=True),
        sa.CheckConstraint("true", name="no_self_favorited"),
        sa.ForeignKeyConstraint(
            ["favorite_id"], ["user.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["subscriber_id"], ["user.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("favorite_id", "subscriber_id"),
        sa.UniqueConstraint(
            "favorite_id", "subscriber_id", name="unique_favorite"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("favorites")
    # ### end Alembic commands ###