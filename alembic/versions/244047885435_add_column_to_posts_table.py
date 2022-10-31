"""Add content column

Revision ID: 244047885435
Revises: bcb92e52ee28
Create Date: 2022-10-29 18:18:35.275820

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = '244047885435'
down_revision = 'bcb92e52ee28'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(),  nullable=False))
    op.add_column("posts", sa.Column('published', sa.Boolean(), server_default="True", nullable=False))
    op.add_column("posts", sa.Column('Created_at', sa.TIMESTAMP(timezone=True), 
                          server_default=sa.text("now()"), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'Created_at')

