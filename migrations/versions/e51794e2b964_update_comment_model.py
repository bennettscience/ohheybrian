"""update comment model

Revision ID: e51794e2b964
Revises: 8d23dd4465a3
Create Date: 2024-01-01 21:32:49.522385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e51794e2b964'
down_revision = '8d23dd4465a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(length=128), nullable=True))
        batch_op.drop_column('website')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website', sa.VARCHAR(length=128), nullable=True))
        batch_op.drop_column('url')

    # ### end Alembic commands ###