"""create_user_table

Revision ID: 3fe3d1c74fd5
Revises:
Create Date: 2017-03-20 16:29:06.477247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e1128c78956'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=False),
        sa.Column('account_id', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('birth_date', sa.Date, nullable=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('designation', sa.String(255), nullable=True),
        sa.Column('landline_number', sa.String(255), nullable=True),
        sa.Column('mobile_number', sa.String(255), nullable=True),
        sa.Column('image_url', sa.String(255), nullable=True),
        sa.Column('status', sa.String(255), nullable=True),
        sa.Column('is_subscribed', sa.Boolean(), nullable=True),
        sa.Column('created_date', sa.DateTime, nullable=False),
        sa.Column('updated_date', sa.DateTime, nullable=True),
        sa.Column('deleted_date', sa.DateTime, nullable=True)
    )


def downgrade():
    op.drop_table('users')
