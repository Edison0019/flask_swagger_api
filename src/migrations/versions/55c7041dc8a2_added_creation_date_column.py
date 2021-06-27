"""added creation date column

Revision ID: 55c7041dc8a2
Revises: 21de5e8e940d
Create Date: 2021-06-26 21:32:50.143291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55c7041dc8a2'
down_revision = '21de5e8e940d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.add_column(sa.Column('creation_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_column('creation_date')

    # ### end Alembic commands ###
