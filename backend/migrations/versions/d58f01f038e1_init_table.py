"""init_table

Revision ID: d58f01f038e1
Revises: 
Create Date: 2023-04-04 15:17:27.226259

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'd58f01f038e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
                    sa.Column('modified_at', sa.DateTime(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column(
                        'id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('role_name', sqlmodel.sql.sqltypes.AutoString(),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users',
                    sa.Column('modified_at', sa.DateTime(), nullable=False),
                    sa.Column('username', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column(
                        'id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(),
                              nullable=False),
                    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('client',
                    sa.Column('modified_at', sa.DateTime(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column(
                        'user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column(
                        'name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column(
                        'address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('postal_address',
                              sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column(
                        'tin', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('user_id')
                    )
    op.create_table('manager',
                    sa.Column('modified_at', sa.DateTime(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column(
                        'user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(),
                              nullable=False),
                    sa.Column('second_name', sqlmodel.sql.sqltypes.AutoString(),
                              nullable=False),
                    sa.Column('patronym', sqlmodel.sql.sqltypes.AutoString(),
                              nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('user_id')
                    )
    op.create_table('user_role',
                    sa.Column('modified_at', sa.DateTime(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('users_id', sqlmodel.sql.sqltypes.AutoString(),
                              nullable=False),
                    sa.Column(
                        'role_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
                    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('users_id', 'role_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('manager')
    op.drop_table('client')
    op.drop_table('users')
    op.drop_table('role')
    # ### end Alembic commands ###
