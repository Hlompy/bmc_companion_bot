"""initial models

Revision ID: 72e4b471e41b
Revises: 
Create Date: 2022-12-27 10:03:02.391844

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "72e4b471e41b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "meeting_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meeting_types")),
        sa.UniqueConstraint("name", name=op.f("uq_meeting_types_name")),
    )
    op.create_table(
        "user_roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_roles")),
        sa.UniqueConstraint("name", name=op.f("uq_user_roles_name")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("first_name", sa.String(length=150), nullable=True),
        sa.Column("last_name", sa.String(length=150), nullable=True),
        sa.Column("middle_name", sa.String(length=150), nullable=True),
        sa.Column("birthday", sa.DateTime(), nullable=True),
        sa.Column("phone", sa.SmallInteger(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("telegram_id", sa.Integer(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"], ["user_roles.id"], name=op.f("fk_users_role_id_user_roles")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_table(
        "meetings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("target_test_score", sa.SmallInteger(), nullable=False),
        sa.Column("time_slot", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["client_id"], ["users.id"], name=op.f("fk_meetings_client_id_users")
        ),
        sa.ForeignKeyConstraint(
            ["type_id"], ["meeting_types.id"], name=op.f("fk_meetings_type_id_meeting_types")
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_meetings_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meetings")),
    )
    op.create_table(
        "meeting_feedbacks_completed",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("meeting_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["meeting_id"],
            ["meetings.id"],
            name=op.f("fk_meeting_feedbacks_completed_meeting_id_meetings"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_meeting_feedbacks_completed_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meeting_feedbacks_completed")),
    )
    op.execute("INSERT INTO meeting_types (id, created_at, name) VALUES (1, NOW(), 'internal')")
    op.execute("INSERT INTO meeting_types (id, created_at, name) VALUES (2, NOW(), 'online')")
    op.execute("INSERT INTO user_roles (id, created_at, name) VALUES (1, NOW(), 'root')")
    op.execute("INSERT INTO user_roles (id, created_at, name) VALUES (2, NOW(), 'admin')")
    op.execute("INSERT INTO user_roles (id, created_at, name) VALUES (3, NOW(), 'user')")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("meeting_feedbacks_completed")
    op.drop_table("meetings")
    op.drop_table("users")
    op.drop_table("user_roles")
    op.drop_table("meeting_types")
    # ### end Alembic commands ###