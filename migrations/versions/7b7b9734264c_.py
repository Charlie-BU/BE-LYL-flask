"""empty message

Revision ID: 7b7b9734264c
Revises: c724ca502759
Create Date: 2025-07-18 23:51:41.289847

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7b7b9734264c'
down_revision = 'c724ca502759'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_pkg', schema=None) as batch_op:
        batch_op.alter_column('features',
               existing_type=mysql.TEXT(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_pkg', schema=None) as batch_op:
        batch_op.alter_column('features',
               existing_type=mysql.TEXT(),
               nullable=False)

    # ### end Alembic commands ###
