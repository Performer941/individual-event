from flask import jsonify, request, session

from models import db
from models.models import Comment
from . import detail_blu


@detail_blu.route("/detail/comment", methods=["POST"])
def detail_comment():
    # 获取评论和用户数据
    news_id = request.json.get('news_id')
    content = request.json.get('content')
    user_id = session.get('user_id')

    # 保存进数据库
    new_comment = Comment()
    new_comment.news_id = news_id
    new_comment.content = content
    new_comment.user_id = user_id
    db.session.add(new_comment)
    db.session.commit()

    ret = {
        "errno": 0,
        "errmsg": "成功"
    }
    return jsonify(ret)
