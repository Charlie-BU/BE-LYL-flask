"""empty message

Revision ID: dacfd6643c0d
Revises: 281831116932
Create Date: 2025-05-18 20:51:37.983347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dacfd6643c0d'
down_revision = '281831116932'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_buyer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coop_talent_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_buyer', schema=None) as batch_op:
        batch_op.drop_column('coop_talent_id')

    # ### end Alembic commands ###
