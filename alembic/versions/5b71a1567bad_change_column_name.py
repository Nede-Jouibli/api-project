"""change column name

Revision ID: 5b71a1567bad
Revises: f7b9cb1ef14c
Create Date: 2022-12-31 11:33:29.959861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b71a1567bad'
down_revision = 'f7b9cb1ef14c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'decision_makers', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'decision_makers', type_='unique')
    # ### end Alembic commands ###
