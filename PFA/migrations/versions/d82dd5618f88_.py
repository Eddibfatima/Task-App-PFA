"""empty message

Revision ID: d82dd5618f88
Revises: 
Create Date: 2023-06-12 17:05:41.359152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd82dd5618f88'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('finished_task', sa.String(length=20), nullable=True))
        batch_op.drop_column('finshed_task')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('finshed_task', sa.VARCHAR(length=20), nullable=True))
        batch_op.drop_column('finished_task')

    # ### end Alembic commands ###