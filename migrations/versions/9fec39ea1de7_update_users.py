"""update users

Revision ID: 9fec39ea1de7
Revises: 
Create Date: 2018-05-12 18:02:46.302619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fec39ea1de7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sport',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=2048), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sport_description'), 'sport', ['description'], unique=False)
    op.create_index(op.f('ix_sport_name'), 'sport', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.Column('city', sa.String(length=32), nullable=True),
    sa.Column('picture', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=False),
    sa.Column('when', sa.Date(), nullable=False),
    sa.Column('sport_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sport_id'], ['sport.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'sport_id', 'user_id')
    )
    op.create_index(op.f('ix_event_name'), 'event', ['name'], unique=True)
    op.create_index(op.f('ix_event_status'), 'event', ['status'], unique=False)
    op.create_index(op.f('ix_event_when'), 'event', ['when'], unique=False)
    op.create_table('user_sport',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('sport_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sport_id'], ['sport.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('event_user_invitations',
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_user_invitations')
    op.drop_table('user_sport')
    op.drop_index(op.f('ix_event_when'), table_name='event')
    op.drop_index(op.f('ix_event_status'), table_name='event')
    op.drop_index(op.f('ix_event_name'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_sport_name'), table_name='sport')
    op.drop_index(op.f('ix_sport_description'), table_name='sport')
    op.drop_table('sport')
    # ### end Alembic commands ###