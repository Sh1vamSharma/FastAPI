"""create post table

Revision ID: bcb92e52ee28
Revises: 
Create Date: 2022-10-29 18:06:03.004579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcb92e52ee28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer, nullable=False, primary_key=True), 
                            sa.Column('title', sa.String, nullable=False))  
                                                                                         


def downgrade() -> None:
    op.drop_table("posts")
