"""Added image table

Revision ID: 68d047582669
Revises: 
Create Date: 2023-03-02 17:51:33.997844

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '68d047582669'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('face_app_images',
    sa.Column('Image id', sa.Integer(), nullable=False),
    sa.Column('Path to an image', sa.String(), nullable=True),
    sa.Column('Face++ request id', sa.String(), nullable=True),
    sa.Column('List of found faces', postgresql.ARRAY(sa.JSON()), nullable=True),
    sa.Column('Number of faces', sa.Integer(), nullable=True),
    sa.Column('Face++ image id', sa.String(), nullable=True),
    sa.Column('Time used by Face++', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('Image id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('face_app_images')
    # ### end Alembic commands ###
