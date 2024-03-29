"""empty message

Revision ID: 4fd0f3b7c7e8
Revises: 3fd4364d9d38
Create Date: 2023-05-12 11:09:08.862623

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4fd0f3b7c7e8"
down_revision = "3fd4364d9d38"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "ordprodopt", "fk_options_product", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "ordprodopt", "fk_order_product", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "ordprodopt", "fk_order_product", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "ordprodopt", "fk_options_product", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###
