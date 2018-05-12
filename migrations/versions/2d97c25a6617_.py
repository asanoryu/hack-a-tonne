"""empty message

Revision ID: 2d97c25a6617
Revises: 057c66fb24c2
Create Date: 2018-05-12 20:35:16.306458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d97c25a6617'
down_revision = '057c66fb24c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('match', sa.Column('timest', sa.Date(), nullable=False))
    op.create_index(op.f('ix_match_timest'), 'match', ['timest'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_match_timest'), table_name='match')
    op.drop_column('match', 'timest')
    # ### end Alembic commands ###
