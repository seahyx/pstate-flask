"""empty message

Revision ID: 76e29f2f4a35
Revises: 51defad68f16
Create Date: 2020-02-04 20:08:25.308362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76e29f2f4a35'
down_revision = '51defad68f16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('hp', sa.String(length=8), nullable=True))
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_hp'), 'user', ['hp'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_hp'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_column('user', 'hp')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
