import json
from config import APPID, APPSECRET
from exts import db
import requests
from datetime import datetime, timedelta


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
    data_post = {
        "touser": User.query.get(user_id).openid,
        "template_id": template_id,
        "lang": 'zh_CN',
        "miniprogramState": 'formal',
        "data": data,
    }
    res = requests.post(url=url, json=data_post, headers={'Content-Type': 'application/json'})
    return 200 if res.json()['errcode'] == 0 else res.json()['errcode']


# 通过rid查询报错信息
def get_rid_info(rid):
    url = "https://api.weixin.qq.com/cgi-bin/openapi/rid/get?access_token=" + get_access_token()
    res = requests.post(url=url, json={"rid": rid}, headers={'Content-Type': 'application/json'})
    print(res.text)
    return eval(res.text)['errmsg']
