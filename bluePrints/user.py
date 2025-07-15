import base64
import os, oss2
import time
from flask import Blueprint, request, jsonify
from sqlalchemy import and_, or_

from decorator import with_app_context
from hooks import *
from config import *
from models import TpUser

bp = Blueprint("user", __name__, url_prefix="/user")

# 初始化阿里云OSS Bucket
auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)


# 字符串编码
def encode(input_string):
    byte_string = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(byte_string)
    encoded_string = base64_bytes.decode()
    return encoded_string


# 字符串解码
def decode(encoded_string):
    base64_bytes = encoded_string.encode('utf-8')
    byte_string = base64.b64decode(base64_bytes)
    decoded_string = byte_string.decode()
    return decoded_string


# 获取用户openid
@bp.route("/fetch_openid", methods=["POST"])
def fetch_openid():
    code = request.json["code"]
    appid = APPID
    app_secret = APPSECRET
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={app_secret}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    data = response.json()
    if "openid" in data:
        return jsonify({
            'status': 200,
            'message': '用户openid获取成功',
            'openid': data["openid"],
        })
    else:
        return jsonify({
            'status': -1,
            'message': '用户openid获取失败',
            'openid': None,
        })


# 储存用户openid
@bp.route("/store_openid", methods=['POST'])
def store_openid():
    data = request.json
    me = TpUser.query.get(data['my_id'])
    me.openid = data['openid']
    db.session.commit()
    return jsonify({
        "status": 200,
        "messages": "openid储存成功"
    })


# 更新last_login时间戳
@bp.route('/update_last_login', methods=['POST'])
def update_last_login():
    user_id = request.json.get("user_id")
    me = TpUser.query.get(user_id)
    me.last_login = time.time()
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "success",
    })


# 处理并发送新消息通知
@bp.route('/send_notification', methods=['POST'])
def send_notification(description='新消息通知'):
    data_request = request.json
    sender_id = data_request['my_id']
    receiver_id = data_request['receiver_id']
    template_id = "8AMX7lHwjpeH4uN-6XslAmSDJhcbbsJcB_RLdIcQZ4o"
    sender = TpUser.query.get(sender_id)
    data = {
        "thing1": {  # 发送人
            "value": sender.realname if sender.realname else sender.nickname,
        },
        "time2": {  # 发送时间
            "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "thing6": {  # 备注
            "value": description,
        },
    }
    res = inform(receiver_id, template_id, data)
    if res == 200:
        return jsonify({
            "message": "success",
            "status": 200,
            "res_status": res,
        })
    return jsonify({
        "message": "fail",
        "status": -1,
        "res_status": res,
    })


# 计算用户个人评分（简历完成度 + 用户活跃度 + 客户满意度）
@bp.route('/calc_star_as_elite', methods=['POST'])
def calc_star_as_elite():
    user_id = request.json['user_id']
    user = TpUser.query.get(user_id)
    # INDEX1-简历评分
    resume = TpItem.query.filter(and_(TpItem.user_id == user_id, TpItem.type == 2)).first()
    resume_score = 0
    # 有简历（发布成功）：40分；三个指标：每个20分
    if resume and (resume.status in [1, 3]):
        resume_score = 40
        index = ['strength', 'experience']
        for key in index:
            if getattr(resume, key, None):  # 如果resume中的字段有key不为None；若无key，则返回None
                resume_score += 20
        # 拿到简历作品，有则加20
        works = ItemFiles.query.get(resume.id)
        if works and works.length > 0:
            resume_score += 20
    # INDEX2-用户活跃度
    active_score = user.active_score
    # INDEX3-客户满意度
    cooperation_evaluate_score = user.cooperation_evaluate_score
    overall_score = resume_score / 100 * 50 + active_score / 100 * 20 + cooperation_evaluate_score / 5 * 30
    user.star_as_elite = overall_score
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


@bp.route('/get_user_star', methods=['POST'])
def get_user_star():
    user_id = request.json['user_id']
    user = TpUser.query.get(user_id)
    username = user.realname if user.realname else user.nickname
    star_as_elite = user.star_as_elite if user.star_as_elite else 0
    cooperation_evaluate_score = user.cooperation_evaluate_score if user.cooperation_evaluate_score else 0
    return jsonify({
        "user_id": user_id,
        "username": username,
        "star_as_elite": star_as_elite,
        "cooperation_evaluate_score": cooperation_evaluate_score,
        "message": "success",
        "status": 200,
    })


# 个人简历相关接口
@bp.route('/upload_works_to_OSS', methods=['POST'])
def upload_works_to_OSS():
    if not request.files.get('this_one'):
        return jsonify({
            "message": "fail: no works",
            "status": -1,
        })
    this_one = request.files['this_one']
    # 保存文件到临时路径
    temp_dir = os.path.join(os.getcwd(), 'tmp_for_works')  # 在当前工作目录创建 'tmp' 文件夹
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, this_one.filename)  # 构建临时文件路径
    this_one.save(temp_path)
    try:
        # 上传到OSS
        oss_path = f'user_works/{this_one.filename}'  # 阿里云目录路径
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


@bp.route('/get_item_id', methods=['POST'])
def get_item_id():
    data = request.json
    user_id = data.get('user_id')
    salary = data.get('salary')  # 简历有这个字段
    title = data.get('title')  # 项目有这个字段
    if salary:
        item = TpItem.query.filter_by(user_id=user_id, salary=salary).first()
        return jsonify({
            "message": "success",
            "status": 200,
            "item_id": item.id,
        })
    elif title:
        item = TpItem.query.filter_by(user_id=user_id, title=title).first()
        return jsonify({
            "message": "success",
            "status": 200,
            "item_id": item.id,
        })
    else:
        return jsonify({
            "message": "fail: can't find item",
            "status": -1,
            "item_id": None,
        })


@bp.route('/get_item_files', methods=['POST'])
def get_item_files():
    data = request.json
    item_id = data.get('item_id')
    item_files = ItemFiles.query.get(item_id)
    if not item_files:
        return jsonify({
            "message": "fail",
            "status": -1,
        })
    return jsonify({
        "message": "success",
        "status": 200,
        "item_files": ItemFiles.to_json(item_files),
    })


# 上传作品
@bp.route('/upload_works', methods=['POST'])
def upload_works():
    data = request.json
    item_id = data['item_id']
    item_type = data['item_type']
    files = data.get('files', [])
    # 动态填充 file1 到 file9，超出范围的设置为 None
    file_fields = [files[i] if i < len(files) else None for i in range(9)]
    item_files = ItemFiles.query.get(item_id)
    if item_files:
        item_files.type = item_type
        item_files.file1 = file_fields[0],
        item_files.file2 = file_fields[1],
        item_files.file3 = file_fields[2],
        item_files.file4 = file_fields[3],
        item_files.file5 = file_fields[4],
        item_files.file6 = file_fields[5],
        item_files.file7 = file_fields[6],
        item_files.file8 = file_fields[7],
        item_files.file9 = file_fields[8],
        item_files.length = len(files)
    else:
        item_files = ItemFiles(
            id=item_id,
            type=item_type,
            file1=file_fields[0],
            file2=file_fields[1],
            file3=file_fields[2],
            file4=file_fields[3],
            file5=file_fields[4],
            file6=file_fields[5],
            file7=file_fields[6],
            file8=file_fields[7],
            file9=file_fields[8],
            length=len(files)
        )
        db.session.add(item_files)
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


# 发布项目相关接口
@bp.route('/upload_project_image_to_OSS', methods=['POST'])
def upload_project_image_to_OSS():
    if not request.files.get('this_one'):
        return jsonify({
            "message": "fail: no works",
            "status": -1,
        })
    this_one = request.files['this_one']
    # 保存文件到临时路径
    temp_dir = os.path.join(os.getcwd(), 'tmp_for_projects')  # 在当前工作目录创建 'tmp' 文件夹
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, this_one.filename)  # 构建临时文件路径
    this_one.save(temp_path)
    try:
        # 上传到OSS
        oss_path = f'project_images/{this_one.filename}'  # 阿里云目录路径
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


@bp.route('/delete_item', methods=['POST'])
def delete_item():
    data = request.json
    item_id = data.get('item_id')
    user_id = data.get('user_id')
    item = TpItem.query.get(item_id)
    item_files = ItemFiles.query.get(item_id)
    if item:
        if item.user_id != user_id:
            return jsonify({
                "message": "unauthorized",
                "status": -1,
            })
        db.session.delete(item)
        if item_files:
            prefix = f'https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/'
            url_list = [item_files.file1, item_files.file2, item_files.file3, item_files.file4,
                        item_files.file5,
                        item_files.file6, item_files.file7, item_files.file8, item_files.file9]
            for url in url_list:
                try:
                    bucket.delete_object(url[len(prefix):])
                except Exception:
                    pass
            db.session.delete(item_files)
        db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


# 拿到该人的全部项目
@bp.route('/get_his_items', methods=['POST'])
def get_his_items():
    data = request.json
    user_id = data.get('user_id')
    items = (TpItem.query.filter(and_(
        TpItem.user_id == user_id,
        TpItem.type == 1
    )).all())
    items = [[item.id, item.title] for item in items]
    return jsonify({
        "message": "success",
        "status": 200,
        "items": items,
    })


@bp.route('/get_evaluate_items_Im_buyer', methods=['POST'])
def get_evaluate_items_Im_buyer():
    data = request.json
    my_id = data.get('my_id')
    to_id = data.get('to_id')
    items = TpItem.query.filter(and_(
        TpItem.user_id == to_id,
        TpItem.type == 1,
        or_(
            TpItem.cooperator1_id == my_id,
            TpItem.cooperator2_id == my_id,
            TpItem.cooperator3_id == my_id,
            TpItem.cooperator4_id == my_id,
            TpItem.cooperator5_id == my_id,
        ),
        TpItem.is_evaluated == 0,
    )).all()
    items = [[item.id, item.title] for item in items]
    return jsonify({
        "message": "success",
        "status": 200,
        "items": items,
    })


@bp.route('/get_evaluate_items_Im_seller', methods=['POST'])
def get_evaluate_items_Im_seller():
    data = request.json
    my_id = data.get('my_id')
    to_id = data.get('to_id')
    items = TpItem.query.filter(and_(
        TpItem.user_id == my_id,
        TpItem.type == 1,
        or_(
            TpItem.cooperator1_id == to_id,
            TpItem.cooperator2_id == to_id,
            TpItem.cooperator3_id == to_id,
            TpItem.cooperator4_id == to_id,
            TpItem.cooperator5_id == to_id,
        ),
    )).all()
    items = [[item.id, item.title] for item in items]
    return jsonify({
        "message": "success",
        "status": 200,
        "items": items,
    })


# 合作评价
@bp.route('/cooperation_evaluate', methods=['POST'])
def cooperation_evaluate():
    data = request.json
    my_id = data.get('my_id')
    to_id = data.get('to_id')
    item_id = data.get('item_id')
    evaluateIndex1 = data.get("evaluateIndex1")
    evaluateIndex2 = data.get("evaluateIndex2")
    if not my_id or not to_id:
        return jsonify({
            "message": "评价者不存在，请稍后再试",
            "status": -1,
        })
    item = TpItem.query.get(item_id)
    if item.is_evaluated:  # 如果项目方已评价过，则必然是人才方先行评价，项目方此时正在评价，这时解除双方合作关系
        for i in range(1, 6):
            cooperator_attr = f"cooperator{i}_id"
            # 检查合作关系是否存在
            if getattr(item, cooperator_attr, None) == to_id:
                # 移除合作关系
                setattr(item, cooperator_attr, None)
                db.session.commit()
    ave_score = (float(evaluateIndex1) + float(evaluateIndex2)) / 2
    user = TpUser.query.get(to_id)
    user.cooperation_evaluate_score = format(((float(user.cooperation_evaluate_score) + ave_score) / 2), ".2f")
    item.is_evaluated = 1
    db.session.commit()
    return jsonify({
        "message": "success",
        "status": 200,
    })


@bp.route('/edit_user_resume', methods=['POST'])
def edit_user_resume():
    data = request.json
    userId = data.get('user_id')
    type = data.get('type')
    birthday = data.get('birthday')
    citys = data.get('citys')
    experience = data.get('experience')
    is_evaluated = data.get('is_evaluated')
    post = data.get('post')
    property = data.get('property')
    remark = data.get('remark')
    salary = data.get('salary')
    salary_unit = data.get('salary_unit')
    sex = data.get('sex')
    strength = data.get('strength')
    tags = data.get('tags')
    talents = data.get('talents')

    exist_item = TpItem.query.filter_by(user_id=userId, type=type).first()
    if exist_item:
        exist_item.birthday = birthday
        exist_item.citys = citys
        exist_item.experience = experience
        exist_item.is_evaluated = is_evaluated
        exist_item.post = post
        exist_item.property = property
        exist_item.remark = remark
        exist_item.salary = salary
        exist_item.salary_unit = salary_unit
        exist_item.sex = sex
        exist_item.strength = strength
        exist_item.tags = tags
        exist_item.talents = talents
        exist_item.status = -1
    else:
        new_item = TpItem(
            user_id=userId,
            type=type,
            birthday=birthday,
            citys=citys,
            experience=experience,
            is_evaluated=is_evaluated,
            post=post,
            property=property,
            remark=remark,
            salary=salary,
            salary_unit=salary_unit,
            sex=sex,
            strength=strength,
            tags=tags,
            talents=talents,
            status=-1
        )
        db.session.add(new_item)
    db.session.commit()
    return jsonify({
        "status": 200,
        "message": "用户简历新增 / 修改成功",
    })


# 为解决php新用户注册问题，新加接口
@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    # 解密手机号
    user_info = decrypt_wechat_data(
        data['encryptedData'],
        data['iv'],
        data['session_key']
    )
    if not user_info:
        return jsonify({'code': 400, 'msg': '解密手机号失败'})

    phone = user_info['purePhoneNumber']
    openid = data.get('xcx_openid')

    # 查库确认是否已经存在用户
    user = db.session.query(TpUser).filter_by(openid=openid).first()
    if user:
        return jsonify({'status': -1, 'message': "用户已注册"})

    # 创建新用户
    user = TpUser(
        phone=phone,
        openid=openid,
        user_token=get_token(),
        is_kf=0,
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'status': 200,
        'message': "用户注册成功",
        "user_id": user.id,
        "user_token": user.user_token
    })
