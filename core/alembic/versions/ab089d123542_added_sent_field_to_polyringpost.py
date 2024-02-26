"""added sent field to polyringpost

Revision ID: ab089d123542
Revises: da3dc6950230
Create Date: 2024-02-26 16:22:57.693223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab089d123542'
down_revision: Union[str, None] = 'da3dc6950230'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('polyringpost', sa.Column('sent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('polyringpost', 'sent')
    # ### end Alembic commands ###