"""Initial migration

Revision ID: 2a53d9419b3e
Revises: 
Create Date: 2019-04-02 22:25:33.338183

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2a53d9419b3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('post',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_by_user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('post_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_by_user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id', 'post_id')
    )
    op.create_table('instrument',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('model', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('eluent',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    )
    op.create_table('column',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    )
    op.create_table('method',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('technique', sa.String(length=80), nullable=False),
    sa.Column('comment', sa.String(length=80), nullable=False),
    sa.Column('analysis_method', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.Column('eluent_a_id', postgresql.UUID, sa.ForeignKey("eluent.id")),
    sa.Column('eluent_b_id', postgresql.UUID, sa.ForeignKey("eluent.id")),
    sa.Column('instrument_id', postgresql.UUID, sa.ForeignKey("instrument.id")),
    )
    op.create_table('compound',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('iupac', sa.String(length=80), nullable=False),
    sa.Column('method_id', postgresql.UUID, sa.ForeignKey("method.id")),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('iupac'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('user')
    op.drop_table('instrument')
    op.drop_table('eluent')
    op.drop_table('column')
    op.drop_table('method')
    op.drop_table('compound')
    # ### end Alembic commands ###
