"""add spam bool to comment model

Revision ID: 36c18955906f
Revises: e51794e2b964
Create Date: 2024-01-02 20:50:23.098285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36c18955906f'
down_revision = 'e51794e2b964'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_spam', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('is_spam')

    # ### end Alembic commands ###
