"""empty message

Revision ID: 0d2523c0cb8a
Revises: d278dee35f5a
Create Date: 2017-12-13 19:29:39.010490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d2523c0cb8a'
down_revision = 'd278dee35f5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.TEXT(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('auther_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['auther_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Post_timestamp'), 'Post', ['timestamp'], unique=False)
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    op.drop_index(op.f('ix_Post_timestamp'), table_name='Post')
    op.drop_table('Post')
    # ### end Alembic commands ###
