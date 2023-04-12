"""empty message

Revision ID: 4933d23d50cc
Revises: eb8a5565f420
Create Date: 2023-04-11 09:52:10.224457

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4933d23d50cc"
down_revision = "eb8a5565f420"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "production_option",
        sa.Column("option_sets", sa.JSON(none_as_null=True), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("production_option", "option_sets")
    # ### end Alembic commands ###
