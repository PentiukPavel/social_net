"""empty message

Revision ID: e290c373276a
Revises: 
Create Date: 2024-10-30 11:51:34.680450

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import URLType


# revision identifiers, used by Alembic.
revision: str = "e290c373276a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("url_avatar", URLType(), nullable=True),
        sa.Column(
            "sex", sa.Enum("MALE", "FEMALE", name="usersex"), nullable=True
        ),
        sa.Column("registered_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    # ### end Alembic commands ###