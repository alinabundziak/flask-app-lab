
"""Insert data into products table

Revision ID: 177254e3dcc7
Revises: 57ffa5de865c
Create Date: 2026-11-18 20:07:01.483769
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '177254e3dcc7'
down_revision = '57ffa5de865c'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    categories = sa.table(
        'categories',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String)
    )

    products = sa.table(
        'products',
        sa.column('name', sa.String),
        sa.column('price', sa.Float),
        sa.column('active', sa.Boolean),
        sa.column('category_id', sa.Integer)
    )

    # Додаємо категорії
    op.bulk_insert(categories, [
        {'name': 'Electronics'},
        {'name': 'Books'},
        {'name': 'Clothing'}
    ])

    # Отримуємо ID категорій
    category_ids = {}

    for name in ['Electronics', 'Books', 'Clothing']:
        category_ids[name] = connection.execute(
            sa.select(categories.c.id).where(
                categories.c.name == name
            )
        ).scalar_one()

    # Додаємо товари
    op.bulk_insert(products, [
        {
            'name': 'Laptop',
            'price': 1200.0,
            'active': True,
            'category_id': category_ids['Electronics']
        },
        {
            'name': 'Smartphone',
            'price': 800.0,
            'active': True,
            'category_id': category_ids['Electronics']
        },
        {
            'name': 'Novel',
            'price': 20.0,
            'active': True,
            'category_id': category_ids['Books']
        },
        {
            'name': 'T-Shirt',
            'price': 25.0,
            'active': False,
            'category_id': category_ids['Clothing']
        }
    ])


def downgrade():
    connection = op.get_bind()

    products = sa.table(
        'products',
        sa.column('name', sa.String)
    )

    categories = sa.table(
        'categories',
        sa.column('name', sa.String)
    )

    # Видаляємо додані товари
    connection.execute(
        products.delete().where(
            products.c.name.in_([
                'Laptop',
                'Smartphone',
                'Novel',
                'T-Shirt'
            ])
        )
    )

    # Видаляємо додані категорії
    connection.execute(
        categories.delete().where(
            categories.c.name.in_([
                'Electronics',
                'Books',
                'Clothing'
            ])
        )
    )
