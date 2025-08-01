"""empty message

Revision ID: 0c025579e80e
Revises: 34d5ee2c374b
Create Date: 2025-05-13 09:06:34.943268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c025579e80e'
down_revision = '34d5ee2c374b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service_pkg',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('features', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_service_pkg'))
    )
    op.create_table('service_talent',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.Column('talent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['service_id'], ['service_pkg.id'], name=op.f('fk_service_talent_service_id_service_pkg')),
    sa.ForeignKeyConstraint(['talent_id'], ['tp_users.user_id'], name=op.f('fk_service_talent_talent_id_tp_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_service_talent'))
    )
    with op.batch_alter_table('tp_users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bought_service_pkg_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_tp_users_bought_service_pkg_id_service_pkg'), 'service_pkg', ['bought_service_pkg_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tp_users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_tp_users_bought_service_pkg_id_service_pkg'), type_='foreignkey')
        batch_op.drop_column('bought_service_pkg_id')

    op.drop_table('service_talent')
    op.drop_table('service_pkg')
    # ### end Alembic commands ###
