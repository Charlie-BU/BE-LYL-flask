import os

import oss2
from flask import Blueprint, request, jsonify

from config import *
from models import *

bp = Blueprint("application", __name__, url_prefix="/application")
# 初始化阿里云OSS Bucket
auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)


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
    post_id = data['post_id']
    post = Post.query.get(post_id)
    if post.poster_id != data["my_id"]:
        return jsonify({
            "message": "fail: unauthorized",
            "status": -1,
        })
    post_images = Post_image.query.filter_by(post_id=post_id).all()
    prefix = f'https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/'
    for post_image in post_images:
        url_list = [post_image.image1, post_image.image2, post_image.image3, post_image.image4, post_image.image5, post_image.image6, post_image.image7, post_image.image8, post_image.image9]
        for url in url_list:
            try:
                bucket.delete_object(url[len(prefix):])
            except Exception:
                pass
        db.session.delete(post_image)
    Post_comment.query.filter_by(post_id=post_id).delete()
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
    Post_comment_reply.query.filter_by(comment_id=data['comment_id']).delete()
    db.session.delete(comment)
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


# 向阿里云OSS上传图片
@bp.route('/upload_image_to_OSS', methods=['POST'])
def upload_image_to_OSS():
    if 'image' not in request.files:
        return jsonify({
            "message": "fail: no image",
            "status": -1,
        })
    image = request.files['image']
    # 保存文件到临时路径
    temp_dir = os.path.join(os.getcwd(), 'tmp')  # 在当前工作目录创建 'tmp' 文件夹
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, image.filename)  # 构建临时文件路径
    image.save(temp_path)
    try:
        # 上传到OSS
        oss_path = f'post-images/{image.filename}'  # 阿里云目录路径
        with open(temp_path, 'rb') as fileobj:
            bucket.put_object(oss_path, fileobj)
        # 获取文件URL
        file_url = f'https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{oss_path}'
        # 删除临时文件
        os.remove(temp_path)
        return jsonify({
            "url": file_url,
            "message": "success",
            "status": 200,
        })
    except Exception as e:
        return jsonify({
            "message": f"fail: {str(e)}",
            "status": -1,
        })


@bp.route('/send_post', methods=['POST'])
def send_post():
    data = request.json
    new_post = Post(title=data['title'], content=data['content'], poster_id=data['my_id'], likes=0, stars=0)
    db.session.add(new_post)
    db.session.commit()
    this_post_id = Post.query.filter_by(content=data['content']).first().id
    image_urls = data['image_urls']
    if len(image_urls) > 0:
        tmp_lst = []
        for i in range(9):
            tmp_lst.append(image_urls[i] if i < len(image_urls) else '')
        new_post_images = Post_image(post_id=this_post_id, image1=tmp_lst[0], image2=tmp_lst[1], image3=tmp_lst[2], image4=tmp_lst[3], image5=tmp_lst[4], image6=tmp_lst[5], image7=tmp_lst[6],
                                     image8=tmp_lst[7], image9=tmp_lst[8], length=len(image_urls))
        db.session.add(new_post_images)
        db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })

# # 支持多图片上传（可选）
# @bp.route('/upload_multiple_images_to_OSS', methods=['POST'])
# def upload_multiple_images_to_OSS():
#     if 'images' not in request.files:
#         return jsonify({
#             "message": "fail: no images",
#             "status": -1,
#         })
#     files = request.files.getlist('images')  # 获取所有文件
#     uploaded_urls = []
#     temp_dir = '/tmp'
#     os.makedirs(temp_dir, exist_ok=True)
#     for image in files:
#         temp_path = os.path.join(temp_dir, image.filename)
#         try:
#             # 保存文件到临时路径
#             image.save(temp_path)
#             # 自定义 OSS 存储路径
#             oss_path = f'post-images/{image.filename}'
#             with open(temp_path, 'rb') as fileobj:
#                 bucket.put_object(oss_path, fileobj)
#             # 获取文件 URL
#             file_url = f'https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{oss_path}'
#             uploaded_urls.append(file_url)
#             # 删除临时文件
#             os.remove(temp_path)
#         except Exception as e:
#             return jsonify({
#                 "message": f"fail: {str(e)}",
#                 "status": -1,
#             })
#     return jsonify({
#         "urls": uploaded_urls,
#         "message": "success",
#         "status": 200,
#     })
