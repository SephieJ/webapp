"""update_user_table_company

Revision ID: 890f99a6b5cc
Revises: 0e1128c78956
Create Date: 2017-06-06 19:05:27.691889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '890f99a6b5cc'
down_revision = '0e1128c78956'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users', sa.Column('co_name', sa.String(255), nullable=True))

    op.add_column('users', sa.Column('co_info', sa.String(255), nullable=True))
    op.add_column('users',
                  sa.Column('co_business_reg_number',
                            sa.String(255),
                            nullable=True)),

    op.add_column('users',
                  sa.Column('co_office_number', sa.String(255), nullable=True))
    op.add_column('users',
                  sa.Column('co_mobile_number', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('co_name', 'co_info', 'co_business_reg_number',
                   'co_office_number', 'co_mobile_number')
