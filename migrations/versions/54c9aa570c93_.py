"""empty message

Revision ID: 54c9aa570c93
Revises: 925b00d2e086
Create Date: 2016-04-11 21:26:00.080695

"""

# revision identifiers, used by Alembic.
revision = '54c9aa570c93'
down_revision = '925b00d2e086'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posting', sa.Column('filter_addon', sa.Boolean(), nullable=True))
    op.add_column('posting', sa.Column('validation_addon', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posting', 'validation_addon')
    op.drop_column('posting', 'filter_addon')
    ### end Alembic commands ###
