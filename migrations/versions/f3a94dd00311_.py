"""empty message

Revision ID: f3a94dd00311
Revises: de2261176912
Create Date: 2023-02-03 13:03:38.648746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3a94dd00311'
down_revision = 'de2261176912'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('competition', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('archived', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('archived_time', sa.DateTime(), nullable=True))

    with op.batch_alter_table('house', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    with op.batch_alter_table('house_points', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    with op.batch_alter_table('result', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    with op.batch_alter_table('result', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    with op.batch_alter_table('house_points', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    with op.batch_alter_table('house', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('archived_time')
        batch_op.drop_column('archived')

    with op.batch_alter_table('competition', schema=None) as batch_op:
        batch_op.alter_column('archived',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###