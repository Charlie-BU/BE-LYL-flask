from flask import Blueprint, request, jsonify
from pandas.io.json import to_json

from models import *

bp = Blueprint("application", __name__, url_prefix="/application")


@bp.route('/test', methods=['GET'])
def test():
    posts = Post.query.all()
    posts = [Post.to_json(post) for post in posts]
    return jsonify({
        "posts": posts,
        "message": "success",
        "status": 200,
    })


@bp.route('/get_all_posts', methods=['POST'])
def get_all_posts():
    posts = Post.query.order_by(Post.time.desc()).all()
    posts = [Post.to_json(post) for post in posts]
    return jsonify({
        "posts": posts,
        "message": "success",
        "status": 200,
    })


@bp.route('/like_post', methods=['POST'])
def like_post():
    post = Post.query.get(request.json['post_id'])
    post.likes += 1
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


@bp.route('/cancel_like_post', methods=['POST'])
def cancel_like_post():
    post = Post.query.get(request.json['post_id'])
    post.likes -= 1
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })

@bp.route('/get_post_comments', methods=['POST'])
def get_post_comments():
    post = Post.query.get(request.json['post_id'])
    comments = post.comments
    comments = [Post_comment.to_json(comment) for comment in comments]
    return jsonify({
        "comments": comments,
        "message": "success",
        "status": 200,
    })

@bp.route('/send_comment', methods=['POST'])
def send_comment():
    data = request.json
    new_comment = Post_comment(content=data['content'], sender_id=data['my_id'], post_id=data['post_id'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


@bp.route('/get_all_post_comments', methods=['POST'])
def get_all_post_comments():
    data = request.json
    post_id = data['post_id']
    post_comments = Post_comment.query.filter_by(post_id=post_id).order_by(Post_comment.time.desc()).all()
    post_comments = [Post_comment.to_json(comment) for comment in post_comments]
    return jsonify({
        "post_comments": post_comments,
        "message": "success",
        "status": 200,
    })