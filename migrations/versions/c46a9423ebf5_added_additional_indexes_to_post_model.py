"""added additional indexes to Post model

Revision ID: c46a9423ebf5
Revises: 080521e8eb06
Create Date: 2021-02-07 19:58:21.632766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c46a9423ebf5'
down_revision = '080521e8eb06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_post_date_posted'), 'post', ['date_posted'], unique=False)
    op.create_index(op.f('ix_post_title'), 'post', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_title'), table_name='post')
    op.drop_index(op.f('ix_post_date_posted'), table_name='post')
    # ### end Alembic commands ###