"""empty message

Revision ID: da769d875e7a
Revises: 0cdf94f9ebff
Create Date: 2018-01-02 14:19:26.350000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da769d875e7a'
down_revision = '0cdf94f9ebff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('auther_id', sa.Integer(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['auther_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Post_timestamp'), 'Post', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Post_timestamp'), table_name='Post')
    op.drop_table('Post')
    # ### end Alembic commands ###
