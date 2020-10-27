from datetime import datetime

from . import db


class News(db.Model):
    """新闻"""
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)  # 新闻编号
    title = db.Column(db.String(256), nullable=False)  # 新闻标题
    source = db.Column(db.String(64), nullable=False)  # 新闻来源
    digest = db.Column(db.String(512), nullable=False)  # 新闻摘要
    content = db.Column(db.Text, nullable=False)  # 新闻内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    index_image_url = db.Column(db.String(256))  # 新闻列表图片路径
    status = db.Column(db.Integer, default=0)  # 当前新闻状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过
    reason = db.Column(db.String(256))  # 未通过原因，status = -1 的时候使用
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 当前新闻的作者id
    user = db.relationship('User', backref=db.backref('news', lazy='dynamic'))
    # 当前新闻的所有评论
    comments = db.relationship("Comment", lazy="dynamic")


class Category(db.Model):
    """新闻分类"""
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名


class Collection(db.Model):
    __tablename__ = "collection"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)  # 新闻编号
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"), primary_key=True)  # 分类编号
    create_time = db.Column(db.DateTime, default=datetime.now)  # 收藏创建时间


class User(db.Model):
    """用户"""
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    create_time = db.Column(db.DateTime, default=datetime.now)  # 注册时间
    is_admin = db.Column(db.Boolean, default=False)  # 管理员身份
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(  # 性别
        db.Enum(
            "MAN",  # 男
            "WOMAN"  # 女
        ),
        default="MAN"
    )


class Comment(db.Model):
    """评论"""
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 用户id
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"), nullable=False)  # 新闻id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now)  # 记录的更新时间
    user = db.relationship("User", backref="comments")  # 评论的创建者
    # 实现对评论的回复（其实就是自关联）
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))  # 父评论id


class CommentLike(db.Model):
    """
    评论点赞
    评论表 与 用户表之间是多对多关系，因为一个评论可以被多个用户点赞，一个用户也可以点赞多个评论
    所以，此表就相当于Comment与User的 中间表
    """
    __tablename__ = "comment_like"
    comment_id = db.Column("comment_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True)  # 评论编号
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)  # 用户编号

