"""first

Revision ID: dc7a907050ec
Revises: 
Create Date: 2021-05-14 04:22:50.225075

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime as dt


# revision identifiers, used by Alembic.
revision = 'dc7a907050ec'
down_revision = None
branch_labels = None
depends_on = None


date = dt.fromisoformat('1992-10-22')
user_admin = (0, 'admin', 'admin', 'admin', 'admin', date)
right_admin = (0, 0, 2)



def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    rights = op.create_table('rights',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('permission', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('id')
    )
    users = op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('login', sa.VARCHAR(length=255), nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), nullable=False),
    sa.Column('date_birth', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.execute(users.insert(user_admin))
    op.execute(rights.insert(right_admin))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('rights')
    # ### end Alembic commands ###
