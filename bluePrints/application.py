from flask import Blueprint, request, jsonify

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


@bp.route('/get_this_post', methods=['POST'])
def get_this_post():
    post_id = request.json['id']
    post = Post.query.get(post_id)
    return jsonify({
        "post": Post.to_json(post),
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
    data = request.json
    comments = Post_comment.query.filter_by(post_id=data['post_id']).order_by(Post_comment.time.desc()).all()
    comments = [Post_comment.to_json(comment) for comment in comments]
    return jsonify({
        "comments": comments,
        "message": "success",
        "status": 200,
    })


@bp.route('/send_comment', methods=['POST'])
def send_comment():
    data = request.json
    new_comment = Post_comment(content=data['content'], sender_id=data['my_id'], post_id=data['post_id'], likes=0)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


@bp.route('/like_comment', methods=['POST'])
def like_comment():
    comment = Post_comment.query.get(request.json['comment_id'])
    comment.likes += 1
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


@bp.route('/cancel_like_comment', methods=['POST'])
def cancel_like_comment():
    comment = Post_comment.query.get(request.json['comment_id'])
    comment.likes -= 1
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })

@bp.route('/delete_post', methods=['POST'])
def delete_post():
    data = request.json
    post = Post.query.get(data['post_id'])
    if post.poster_id != data["my_id"]:
        return jsonify({
            "message": "fail: unauthorized",
            "status": -1,
        })
    db.session.delete(post)
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


@bp.route('/delete_comment', methods=['POST'])
def delete_comment():
    data = request.json
    comment = Post_comment.query.get(data['comment_id'])
    if comment.sender_id != data["my_id"]:
        return jsonify({
            "message": "fail: unauthorized",
            "status": -1,
        })
    db.session.delete(comment)
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


