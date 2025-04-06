"""add foreign ket to post table

Revision ID: 93326780ee7e
Revises: 0de520eb13b3
Create Date: 2025-04-06 14:28:13.847001

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "93326780ee7e"
down_revision: Union[str, None] = "0de520eb13b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() :
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id") 
    pass
