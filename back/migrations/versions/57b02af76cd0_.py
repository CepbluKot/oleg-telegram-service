"""empty message

Revision ID: 57b02af76cd0
Revises: 
Create Date: 2022-04-27 19:41:13.721814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57b02af76cd0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('days_connecta',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('day', sa.Date(), nullable=True),
    sa.Column('free_items', sa.Integer(), nullable=True),
    sa.Column('staff_free', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('myservice_connecta',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_service', sa.String(), nullable=True),
    sa.Column('price_service', sa.DECIMAL(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mystaff_connecta',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_staff', sa.String(), nullable=True),
    sa.Column('service_staff', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_connectall',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('tg_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.Unicode(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_this_company',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_client', sa.String(), nullable=True),
    sa.Column('tg_id', sa.Integer(), nullable=True),
    sa.Column('phone_num', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('all_booking',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.Time(), nullable=True),
    sa.Column('signup_date', sa.Integer(), nullable=True),
    sa.Column('signup_user', sa.Integer(), nullable=True),
    sa.Column('signup_service', sa.Integer(), nullable=True),
    sa.Column('signup_staff', sa.Integer(), nullable=True),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['signup_date'], ['days_connecta.id'], ),
    sa.ForeignKeyConstraint(['signup_service'], ['myservice_connecta.id'], ),
    sa.ForeignKeyConstraint(['signup_staff'], ['mystaff_connecta.id'], ),
    sa.ForeignKeyConstraint(['signup_user'], ['users_this_company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('all_booking')
    op.drop_table('users_this_company')
    op.drop_table('users_connectall')
    op.drop_table('mystaff_connecta')
    op.drop_table('myservice_connecta')
    op.drop_table('days_connecta')
    # ### end Alembic commands ###
