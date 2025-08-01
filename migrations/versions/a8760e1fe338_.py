"""empty message

Revision ID: a8760e1fe338
Revises: bf9a2745fc86
Create Date: 2025-05-19 11:25:37.325118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8760e1fe338'
down_revision = 'bf9a2745fc86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_pkg', schema=None) as batch_op:
        batch_op.add_column(sa.Column('images', sa.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_pkg', schema=None) as batch_op:
        batch_op.drop_column('images')

    # ### end Alembic commands ###
