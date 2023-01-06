"""fix TestProgress

Revision ID: 3564fbb8381f
Revises: f464f785c3ca
Create Date: 2023-01-05 14:08:06.818276

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3564fbb8381f"
down_revision = "f464f785c3ca"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "test_progress",
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Время удаления"),
    )
    op.create_unique_constraint("unique_progress", "test_progress", ["user_id", "test_question_id"])
    op.add_column(
        "test_questions",
        sa.Column("deleted_at", sa.DateTime(), nullable=True, comment="Время удаления"),
    )
    op.create_unique_constraint(
        "unique_question_in_test", "test_questions", ["test_id", "question_id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("unique_question_in_test", "test_questions", type_="unique")
    op.drop_column("test_questions", "deleted_at")
    op.drop_constraint("unique_progress", "test_progress", type_="unique")
    op.drop_column("test_progress", "deleted_at")
    # ### end Alembic commands ###
