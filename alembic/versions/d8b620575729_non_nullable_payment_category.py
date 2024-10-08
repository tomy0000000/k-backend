"""Non-Nullable Payment Category

Revision ID: d8b620575729
Revises: 00f86965b05a
Create Date: 2022-06-10 16:20:35.346225

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d8b620575729"
down_revision = "00f86965b05a"
branch_labels = None
depends_on = None

payment_category_enum = sa.Enum("Expense", "Income", "Transfer", name="paymentcategory")


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "payment", "category", existing_type=payment_category_enum, nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "payment", "category", existing_type=payment_category_enum, nullable=True
    )
    # ### end Alembic commands ###
