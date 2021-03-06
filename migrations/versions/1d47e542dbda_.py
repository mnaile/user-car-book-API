"""empty message

Revision ID: 1d47e542dbda
Revises: 0ba31c277a0b
Create Date: 2020-07-14 22:19:50.869057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d47e542dbda'
down_revision = '0ba31c277a0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_book_user_id_fkey', 'user_book', type_='foreignkey')
    op.create_foreign_key(None, 'user_book', 'User', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('user_car_user_id_fkey', 'user_car', type_='foreignkey')
    op.create_foreign_key(None, 'user_car', 'User', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_car', type_='foreignkey')
    op.create_foreign_key('user_car_user_id_fkey', 'user_car', 'User', ['user_id'], ['id'])
    op.drop_constraint(None, 'user_book', type_='foreignkey')
    op.create_foreign_key('user_book_user_id_fkey', 'user_book', 'User', ['user_id'], ['id'])
    # ### end Alembic commands ###
