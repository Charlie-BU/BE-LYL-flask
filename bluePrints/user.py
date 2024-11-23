import base64
from flask import Blueprint, request, jsonify
from hooks import *
from models import TpUser

bp = Blueprint("user", __name__, url_prefix="/user")


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


# 处理并发送新消息通知
@bp.route('/send_notification', methods=['POST'])
def send_notification(description='新消息通知'):
    data_request = request.json
    sender_id = data_request['my_id']
    receiver_id = data_request['receiver_id']
    timestamp = data_request['timestamp']
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
