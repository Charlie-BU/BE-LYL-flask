import json, operator, string, random, time, re, base64
from datetime import datetime, timedelta
from flask import Blueprint, request, redirect, url_for, session, render_template, g, jsonify, flash
from sqlalchemy import and_, or_
from exts import db
from wxpay import *
from hooks import inform
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

@bp.route('/get_special_post', methods=['POST'])
def get_special_post():
    post_id = request.json['id']
    post = Post.query.get(post_id)
    return jsonify({
        "post": Post.to_json(post),
        "message": "success",
        "status": 200,
    })

@bp.route('/like_post', methods=['POST'])
def like_post():

    posts = Post.query.order_by(Post.time.desc()).all()
    posts = [Post.to_json(post) for post in posts]
    return jsonify({
        "posts": posts,
        "message": "success",
        "status": 200,
    })