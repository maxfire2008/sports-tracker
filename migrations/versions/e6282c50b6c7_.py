"""empty message

Revision ID: e6282c50b6c7
Revises:
Create Date: 2022-12-27 11:42:06.368975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6282c50b6c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('competition',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('scored', sa.Boolean(), nullable=True),
                    sa.Column('sorting_type', sa.String(), nullable=True),
                    sa.Column('gender', sa.String(), nullable=True),
                    sa.Column('ystart', sa.Integer(), nullable=True),
                    sa.Column('start_time', sa.DateTime(), nullable=True),
                    sa.Column('event_id', sa.Integer(), nullable=True),
                    sa.Column('archived', sa.Boolean(), nullable=True),
                    sa.Column('archived_time', sa.DateTime(), nullable=True),
                    sa.Column('sorting_options', sa.JSON(), nullable=True),
                    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('bonus_points',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('competition_id', sa.Integer(), nullable=True),
                    sa.Column('event_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('house', sa.String(), nullable=True),
                    sa.Column('points', sa.Integer(), nullable=True),
                    sa.Column('archived', sa.Boolean(), nullable=True),
                    sa.Column('archived_time', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['competition_id'], [
                                            'competition.id'], ),
                    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('result',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('competition_id', sa.Integer(), nullable=True),
                    sa.Column('student_id', sa.String(), nullable=True),
                    sa.Column('score', sa.String(), nullable=True),
                    sa.Column('points_awarded', sa.Integer(), nullable=True),
                    sa.Column('place', sa.Integer(), nullable=True),
                    sa.Column('archived', sa.Boolean(), nullable=True),
                    sa.Column('archived_time', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['competition_id'], [
                                            'competition.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('result')
    op.drop_table('bonus_points')
    op.drop_table('competition')
    op.drop_table('event')
    # ### end Alembic commands ###
