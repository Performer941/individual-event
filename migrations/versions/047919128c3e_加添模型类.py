"""‘加添模型类’

Revision ID: 047919128c3e
Revises: f37e63efdca6
Create Date: 2020-10-27 08:16:23.440805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '047919128c3e'
down_revision = 'f37e63efdca6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collection',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('news_id', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['news_id'], ['news.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'news_id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('news_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['news_id'], ['news.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment_like',
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('comment_id', 'user_id')
    )
    op.drop_constraint('news_ibfk_2', 'news', type_='foreignkey')
    op.drop_constraint('news_ibfk_1', 'news', type_='foreignkey')
    op.create_foreign_key(None, 'news', 'category', ['category_id'], ['id'])
    op.create_foreign_key(None, 'news', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'news', type_='foreignkey')
    op.drop_constraint(None, 'news', type_='foreignkey')
    op.create_foreign_key('news_ibfk_1', 'news', 'category', ['category_id'], ['id'], onupdate='RESTRICT', ondelete='RESTRICT')
    op.create_foreign_key('news_ibfk_2', 'news', 'user', ['user_id'], ['id'], onupdate='RESTRICT', ondelete='RESTRICT')
    op.drop_table('comment_like')
    op.drop_table('comment')
    op.drop_table('collection')
    # ### end Alembic commands ###
