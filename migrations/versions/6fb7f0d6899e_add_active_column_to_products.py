
"""Add active column to products

Revision ID: 6fb7f0d6899e
Revises: 1aeeeb362dfa
Create Date: 2026-11-18 19:52:11.426682
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fb7f0d6899e'
down_revision = '1aeeeb362dfa'
branch_labels = None
depends_on = None


def upgrade():
    # Додаємо поле active з початковим значенням True
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'active',
                sa.Boolean(),
                nullable=False,
                server_default=sa.true()
            )
        )


def downgrade():
    # Видаляємо поле active під час відкату міграції
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('active')
