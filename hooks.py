import hashlib
import json
import random
import string

from config import APPID, APPSECRET
from exts import db
import requests
from datetime import datetime, timedelta
from models import *


# 获取（或刷新）access_token
def get_access_token():
    last_token = AccessToken.query.order_by(AccessToken.id.desc()).limit(1).first()
    lost_time = last_token.update_time + timedelta(seconds=last_token.expires_in)
    if datetime.now() < lost_time:
        return last_token.access_token
    grant_type = "client_credential"
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={APPID}&secret={APPSECRET}"
    data = requests.get(url).json()
    token = data['access_token']
    expires_in = data['expires_in']
    access_token = AccessToken(access_token=token, expires_in=expires_in - 60)
    db.session.add(access_token)
    db.session.commit()
    return token


# 发送对应模板的微信通知
def inform(user_id, template_id, data):
    url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=" + get_access_token()
    receiver_openid = TpUser.query.get(user_id).openid
    data_post = {
        "touser": receiver_openid,
        "template_id": template_id,
        "lang": 'zh_CN',
        "miniprogramState": 'formal',
        "data": data,
    }
    res = requests.post(url=url, json=data_post, headers={'Content-Type': 'application/json'})
    print(res.json())
    return 200 if res.json()['errcode'] == 0 else res.json()['errcode']


# 通过rid查询报错信息
def get_rid_info(rid):
    url = "https://api.weixin.qq.com/cgi-bin/openapi/rid/get?access_token=" + get_access_token()
    res = requests.post(url=url, json={"rid": rid}, headers={'Content-Type': 'application/json'})
    print(res.text)
    return eval(res.text)['errmsg']


# 解密微信手机号
from Crypto.Cipher import AES
import base64


def encrypt(s):
    return hashlib.md5(("ZHANGDADA" + s).encode()).hexdigest()


# 生成用户token，对应PHP中的getToken函数
def get_token():
    # 字符集，包含大小写字母和数字
    b = string.ascii_uppercase + string.ascii_lowercase + string.digits

    while True:
        # 生成9位不同的数字和字母
        tmp = []
        while len(tmp) < 9:
            # 随机打乱字符集并取其中一个字符
            chars = list(b)
            random.shuffle(chars)
            tmp.append(chars[random.randint(0, len(b) - 1)])
            # 去重
            tmp = list(set(tmp))

        # 将字符列表连接成字符串
        s = ''.join(tmp)
        # 加密生成user_token
        user_token = encrypt(s)

        # 检查数据库中是否已存在相同的token
        exists = TpUser.query.filter_by(user_token=user_token).first()
        if not exists:
            break

    return user_token


def _unpad(s):
    # 微信加密数据使用的是 PKCS#7 padding
    return s[:-s[-1]]


def decrypt_wechat_data(encrypted_data, iv, session_key):
    try:
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)
        session_key = base64.b64decode(session_key)

        cipher = AES.new(session_key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data)
        decrypted = _unpad(decrypted)  # 去除填充
        decrypted = json.loads(decrypted.decode('utf-8'))
        return decrypted
    except Exception as e:
        print("解密失败:", e)
        return None
