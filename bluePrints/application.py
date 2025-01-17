import os, oss2
from flask import Blueprint, request, jsonify
from sqlalchemy import or_, and_, not_, case
from config import *
from models import *

bp = Blueprint("application", __name__, url_prefix="/application")
# 初始化阿里云OSS Bucket
auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)


@bp.route('/get_posts_by_type', methods=['POST'])
def get_posts_by_type():
    type = request.json['type']
    posts = Post.query.filter_by(type=type).order_by(
        case((Post.starred, 0), else_=1),  # 如果 starred 为 True，则值为 0，否则为 1
        Post.time.desc()
    ).all()
    posts = [Post.to_json(post) for post in posts]
    return jsonify({
        "posts": posts,
        "message": "success",
        "status": 200,
    })


# 推荐帖子优先
@bp.route('/get_all_posts_with_star', methods=['POST'])
def get_all_posts_with_star():
    posts = Post.query.order_by(
        case((Post.starred, 0), else_=1),  # 如果 starred 为 True，则值为 0，否则为 1
        Post.time.desc()
    ).all()
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


@bp.route('/get_post_comments_and_replies', methods=['POST'])
def get_post_comments_and_replies():
    data = request.json
    comments = Post_comment.query.filter_by(post_id=data['post_id']).order_by(Post_comment.time.desc()).all()
    comment_ids = [comment.id for comment in comments]
    comments = [Post_comment.to_json(comment) for comment in comments]
    replies = Post_comment_reply.query.filter(Post_comment_reply.comment_id.in_(comment_ids)).order_by(
        Post_comment_reply.time.desc()).all()
    replies = [Post_comment_reply.to_json(reply) for reply in replies]
    comments_and_replies = sorted(comments + replies, key=lambda ele: ele['time'], reverse=True)
    post = Post.query.get(data['post_id'])
    post.comment_length = len(comments_and_replies)
    db.session.commit()
    return jsonify({
        "comments": comments_and_replies,
        "comment_length": len(comments_and_replies),
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
        "comment_length": len(comments),
        "message": "success",
        "status": 200,
    })


@bp.route('/get_comment_replies', methods=['POST'])
def get_comment_replies():
    data = request.json
    replies = Post_comment_reply.query.filter_by(comment_id=data['comment_id']).order_by(
        Post_comment_reply.time.desc()).all()
    replies = [Post_comment_reply.to_json(reply) for reply in replies]
    return jsonify({
        "replies": replies,
        "reply_length": len(replies),
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


@bp.route('/send_comment_reply', methods=['POST'])
def send_comment_reply():
    data = request.json
    new_comment_reply = Post_comment_reply(content=data['content'], sender_id=data['my_id'], post_id=data['post_id'],
                                           comment_id=data['comment_id'])
    db.session.add(new_comment_reply)
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
    post_images = Post_image.query.filter_by(post_id=post_id).all()
    prefix = f'https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/'
    for post_image in post_images:
        url_list = [post_image.image1, post_image.image2, post_image.image3, post_image.image4, post_image.image5,
                    post_image.image6, post_image.image7, post_image.image8, post_image.image9]
        for url in url_list:
            try:
                bucket.delete_object(url[len(prefix):])
            except Exception:
                pass
        db.session.delete(post_image)
    Post_comment_reply.query.filter_by(post_id=post_id).delete()
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
    Post_comment_reply.query.filter_by(comment_id=data['comment_id']).delete()
    db.session.delete(comment)
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


@bp.route('/delete_comment_reply', methods=['POST'])
def delete_comment_reply():
    data = request.json
    reply = Post_comment_reply.query.get(data['comment_id'])
    if reply.sender_id != data["my_id"]:
        return jsonify({
            "message": "fail: unauthorized",
            "status": -1,
        })
    db.session.delete(reply)
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


@bp.route('/star_post_or_unstar', methods=['POST'])
def star_post_or_unstar():
    data = request.json
    me = TpUser.query.get(data['my_id'])
    if not me.is_kf:
        return jsonify({
            "message": "fail: unauthorized",
            "status": -1,
        })
    post = Post.query.get(data['post_id'])
    post.starred = 0 if post.starred == 1 else 1
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
    try:
        new_post = Post(title=data['title'], content=data['content'], poster_id=data['my_id'], likes=0, starred=0,
                        comment_length=0, type=data['type'])
    except KeyError:
        return jsonify({
            "message": "fail: info insufficient",
            "status": -1,
        })
    db.session.add(new_post)
    db.session.commit()
    this_post_id = Post.query.filter_by(content=data['content']).first().id
    image_urls = data['image_urls']
    if len(image_urls) > 0:
        tmp_lst = []
        for i in range(9):
            tmp_lst.append(image_urls[i] if i < len(image_urls) else '')
        new_post_images = Post_image(post_id=this_post_id, image1=tmp_lst[0], image2=tmp_lst[1], image3=tmp_lst[2],
                                     image4=tmp_lst[3], image5=tmp_lst[4], image6=tmp_lst[5], image7=tmp_lst[6],
                                     image8=tmp_lst[7], image9=tmp_lst[8], length=len(image_urls))
        db.session.add(new_post_images)
        db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


# # 多图片上传（不要这样）
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


# 获取项目的沟通列表
@bp.route('/get_all_item_chats', methods=['POST'])
def get_all_item_chats():
    item_id = request.json["item_id"]
    all_chats = TpItemsChat.query.filter_by(item_id=item_id).order_by(TpItemsChat.update_time.desc()).all()
    all_chats = [TpItemsChat.to_json(all_chat) for all_chat in all_chats]
    return jsonify({
        "all_chats": all_chats,
        "message": "success",
        "status": 200,
    })


# 项目合作
@bp.route('/item_cooperate', methods=['POST'])
def item_cooperate():
    data = request.json
    item_id = data['item_id']
    cooperator_id = data['cooperator_id']
    item = TpItem.query.get(item_id)
    if item.cooperator_id == cooperator_id:
        return jsonify({
            "status": -2,
            "message": "already in cooperate",
        })
    elif item.cooperator_id and item.cooperator_id != cooperator_id:
        return jsonify({
            "status": -1,
            "message": "item occupied",
        })
    item.cooperator_id = cooperator_id
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "success",
    })


@bp.route('/item_terminate_cooperate', methods=['POST'])
def item_terminate_cooperate():
    data = request.json
    item_id = data['item_id']
    item_owner_id = data['item_owner_id']
    item = TpItem.query.get(item_id)
    if item.user_id != item_owner_id:
        return jsonify({
            "status": -1,
            "message": "unauthorized",
        })
    elif not item.cooperator_id:
        return jsonify({
            "status": -2,
            "message": "item not in cooperate",
        })
    item.cooperator_id = None
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "success",
    })