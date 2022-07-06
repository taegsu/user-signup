"""Add Unique option in user_token

Revision ID: 644771cf4694
Revises: a43236b8674f
Create Date: 2022-07-06 10:48:59.807854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '644771cf4694'
down_revision = 'a43236b8674f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_user_token', table_name='user')
    op.create_index(op.f('ix_user_user_token'), 'user', ['user_token'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_user_token'), table_name='user')
    op.create_index('ix_user_user_token', 'user', ['user_token'], unique=False)
    # ### end Alembic commands ###
