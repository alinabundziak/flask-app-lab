
from alembic import op
import sqlalchemy as sa


revision = "e9a80c032fa0"
down_revision = "df3c523d0f93"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.alter_column(
            "user_id",
            existing_type=sa.Integer(),
            nullable=False
        )
        batch_op.drop_column("author")


def downgrade():
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "author",
                sa.String(length=20),
                nullable=False,
                server_default="Anonymous"
            )
        )
        batch_op.alter_column(
            "user_id",
            existing_type=sa.Integer(),
            nullable=True
        )

    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.alter_column(
            "author",
            existing_type=sa.String(length=20),
            server_default=None
        )
