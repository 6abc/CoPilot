"""Add table for case report templates

Revision ID: a1e4beb87498
Revises: ba64d98dbdc5
Create Date: 2024-10-03 10:14:31.289126

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1e4beb87498"
down_revision: Union[str, None] = "ba64d98dbdc5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "incident_management_case_report_template_datastore",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_template_name", sa.String(length=255), nullable=False),
        sa.Column("bucket_name", sa.String(length=255), nullable=False),
        sa.Column("object_key", sa.String(length=1024), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=100), nullable=True),
        sa.Column("file_size", sa.Integer(), nullable=True),
        sa.Column("upload_time", sa.DateTime(), nullable=False),
        sa.Column("file_hash", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("incident_management_case_report_template_datastore")
    # ### end Alembic commands ###