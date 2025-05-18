import base64
import os, oss2
import time
from flask import Blueprint, request, jsonify, session
from oss2 import Service
from sqlalchemy import and_, or_
from hooks import *
from config import *
from models import TpUser
from wxpay import WxPay

bp = Blueprint("service", __name__, url_prefix="/service")


@bp.route("/get_service_categories", methods=["POST"])
def get_service_categories():
    categoires = ServiceCategory.query.all()
    categories = [category.to_json() for category in categoires]
    return jsonify({
        "status": 200,
        "categories": categories,
        "message": "服务包种类获取成功",
    })


@bp.route("/get_all_services", methods=["POST"])
def get_all_services():
    data = request.json
    category_id = data.get("category_id", None)
    try:
        category_id = int(category_id)
    except Exception as e:
        category_id = None
    if category_id:
        services = ServicePkg.query.filter(ServicePkg.category_id == category_id).all()
    else:
        services = ServicePkg.query.all()
    services = [service.to_json() for service in services]
    return jsonify({
        "status": 200,
        "services": services
    })


@bp.route("/get_service_by_id", methods=["POST"])
def get_service_by_id():
    data = request.get_json()
    try:
        service = ServicePkg.query.get(data["id"])
        if not service:
            return jsonify({
                "status": -1,
                "message": "服务包不存在"
            })
        return jsonify({
            "status": 200,
            "service": service.to_json()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": 500,
            "message": "数据获取失败"
        })


@bp.route("/get_my_services", methods=["POST"])
def get_my_services():
    talent_id = request.json.get("talent_id")
    service_talents = Service_talent.query.filter_by(talent_id=talent_id).all()
    services = []
    for service_talent in service_talents:
        service = service_talent.service
        if service:
            services.append(service.to_json())
    return jsonify({
        "status": 200,
        "services": services
    })


@bp.route("/edit_service", methods=["POST"])
def edit_service():
    try:
        data = request.get_json()
        service = ServicePkg.query.get(data.get('id'))

        if not service:
            return jsonify({
                "status": 404,
                "message": "服务包不存在"
            })

        service.name = data.get('name')
        price = data.get('price')
        try:
            price = float(price)
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "请输入正确的价格"
            })
        service.price = price
        service.description = data.get('description')
        features = ServicePkg.concatenate_features(data.get('features'))
        service.features = features
        db.session.commit()

        return jsonify({
            "status": 200,
            "message": "编辑成功"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": 500,
            "message": "服务器错误"
        })


@bp.route("/add_service", methods=["POST"])
def add_service():
    try:
        data = request.get_json()
        price = data.get('price')
        try:
            price = float(price)
        except ValueError:
            return jsonify({
                "status": -1,
                "message": "请输入正确的价格"
            })
        new_service = ServicePkg(
            name=data.get('name'),
            price=price,
            description=data.get('description'),
            features=ServicePkg.concatenate_features(data.get('features')),
            category_id=data.get('category_id'),
        )

        db.session.add(new_service)
        db.session.commit()

        return jsonify({
            "status": 200,
            "message": "添加成功"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": 500,
            "message": "服务器错误"
        })


@bp.route("/delete_service", methods=["POST"])
def delete_service():
    # 获取请求数据中的服务包ID
    data = request.get_json()
    service_id = data.get('id')

    if not service_id:
        return jsonify({
            "status": 400,
            "message": "缺少服务包ID"
        })

    try:
        # 查找并删除服务包
        service = ServicePkg.query.get(service_id)
        if not service:
            return jsonify({
                "status": 404,
                "message": "服务包不存在"
            })

        if service.service_talents:
            for talent in service.service_talents:
                db.session.delete(talent)
        if service.service_buyers:
            for buyer in service.service_buyers:
                db.session.delete(buyer)
        db.session.delete(service)
        db.session.commit()

        return jsonify({
            "status": 200,
            "message": "删除成功"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": 500,
            "message": "删除失败：" + str(e)
        })


@bp.route("/search_user", methods=["POST"])
def search_user():
    # 获取请求数据中的手机号
    data = request.get_json()
    phone = data.get('phone')

    if not phone:
        return jsonify({
            "status": 400,
            "message": "请输入手机号"
        })

    try:
        # 查找用户，使用 filter 而不是 filter_by 来实现模糊查询
        all_users = TpUser.query.filter(TpUser.mobile.like(f"%{phone}%")).all()
        if not all_users:
            return jsonify({
                "status": 404,
                "message": "未找到用户"
            })
        users = []
        for user in all_users:
            users.append({
                "id": user.user_id,
                "name": user.realname,
                "phone": user.mobile,
                "his_service_ids": [st.service_id for st in user.service_talents] if user.service_talents else [],
            })

        # 返回用户信息
        return jsonify({
            "status": 200,
            "users": users
        })

    except Exception as e:
        return jsonify({
            "status": 500,
            "message": "查询失败：" + str(e)
        })


@bp.route("/assign_talent", methods=["POST"])
def assign_talent():
    """
    分配人才接口
    请求参数:
    - service_id: 服务包ID
    - talent_id: 人才ID
    """
    # 获取请求参数
    data = request.json
    service_id = data.get('service_id')
    talent_id = data.get('talent_id')
    # 参数验证
    if not service_id or not talent_id:
        return jsonify({
            'status': 400,
            'message': '参数错误'
        })

    try:
        exist = Service_talent.query.filter(
            and_(Service_talent.service_id == service_id, Service_talent.talent_id == talent_id)).all()
        if len(exist) > 0:
            return jsonify({
                "status": -1,
                "message": "当前服务包已分配该人才"
            })
        service_talent = Service_talent(service_id=service_id, talent_id=talent_id)
        db.session.add(service_talent)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': '分配成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'message': '服务器错误'
        })


@bp.route("/unassign_talent", methods=["POST"])
def unassign_talent():
    # 获取请求参数
    data = request.json
    service_id = data.get('service_id')
    talent_id = data.get('talent_id')
    # 参数验证
    if not service_id or not talent_id:
        return jsonify({
            'status': 400,
            'message': '参数错误'
        })

    try:
        exist = Service_talent.query.filter(
            and_(Service_talent.service_id == service_id, Service_talent.talent_id == talent_id)).first()
        if not exist:
            return jsonify({
                "status": -1,
                "message": "当前服务包未分配该人才"
            })
        db.session.delete(exist)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': '取消分配成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'message': '服务器错误'
        })


@bp.route("/get_talents_by_service", methods=["POST"])
def get_talents_by_service():
    data = request.get_json()
    service_id = data.get('service_id')
    try:
        service_talents = Service_talent.query.filter(Service_talent.service_id == service_id).all()
        serviceTalents = []
        for service_talent in service_talents:
            talent = service_talent.talent
            serviceTalents.append({
                "id": talent.user_id,
                "name": talent.realname,
                "phone": talent.mobile,
            })
        return jsonify({
            "status": 200,
            "serviceTalents": serviceTalents,
            "message": "查询成功"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": 500,
            "message": "查询失败"
        })


# 发起支付
@bp.route('/create_pay', methods=['POST'])
def create_pay():
    data = request.json
    pay_data = {
        'body': data['description'],  # 商品描述
        'attach': data['attach'],  # 附加数据
        'total_fee': int(data['amount'] * 100),  # 金额，单位为分
        'openid': data['openid'],
    }
    wxpay = WxPay(pay_data)
    pay_info = wxpay.get_pay_info()
    if pay_info:
        return jsonify(pay_info)
    return jsonify({
        "status": -1,
        "message": "支付请求发起失败"
    })


@bp.route("/buy_service", methods=["POST"])
def buy_service():
    # 获取请求参数
    data = request.json
    service_id = data.get('service_id')
    buyer_id = data.get('buyer_id')
    amount = data.get('amount', 1)
    # 参数验证
    if not service_id or not buyer_id:
        return jsonify({
            'status': 400,
            'message': '参数错误'
        })
    try:
        service = ServicePkg.query.get(service_id)
        if not service:
            return jsonify({
                "status": -1,
                "message": "未找到服务包"
            })
        buyer = TpUser.query.get(buyer_id)
        if not buyer:
            return jsonify({
                "status": -2,
                "message": "未找到买方用户"
            })
        service_buyer = Service_buyer(service_id=service_id, buyer_id=buyer_id, amount=amount)
        db.session.add(service_buyer)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': '服务包购买成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'message': '服务器错误'
        })


@bp.route("/get_service_I_bought", methods=["POST"])
def get_service_I_bought():
    data = request.get_json()
    my_id = data.get('my_id')
    try:
        sevice_buyers = Service_buyer.query.filter(Service_buyer.buyer_id == my_id).all()
        services = []
        for service_buyer in sevice_buyers:
            service = ServicePkg.query.get(service_buyer.service_id)
            if service:
                service_dict = service.to_json()
                service_dict["amount"] = service_buyer.amount
                # 必须携带service_buyer.id，否则当一人先后多个相同服务包则无法区分
                service_dict["service_buyer_id"] = service_buyer.id
                service_dict["coop_talent_id"] = service_buyer.coop_talent_id
                # 若已确认合作，则只显示合作人才
                if service_buyer.coop_talent_id:
                    coop_talent = TpUser.query.get(service_buyer.coop_talent_id)
                    service_dict["talents"] = [{
                        "id": service_buyer.coop_talent_id,
                        "name": coop_talent.realname,
                        "phone": coop_talent.mobile,
                        "star_as_elite": coop_talent.star_as_elite,
                    }]
                services.append(service_dict)
        return jsonify({
            "status": 200,
            "services": services,
            "message": "查询成功"
        })
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            "status": 500,
            "message": "查询失败"
        })


@bp.route("/get_his_resume_id", methods=["POST"])
def get_his_resume_id():
    data = request.get_json()
    talent_id = data.get('talent_id')
    try:
        his_resume = TpItem.query.filter(TpItem.user_id == talent_id, TpItem.type == 2, TpItem.status == 3).first()
        if not his_resume:
            return jsonify({
                "status": -1,
                "message": "该人才未上传简历或简历未通过审核"
            })
        return jsonify({
            "status": 200,
            "resume_id": his_resume.id,
            "message": "查询成功"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": 500,
            "message": "查询失败"
        })


@bp.route("/confirm_cooperate", methods=["POST"])
def confirm_cooperate():
    data = request.json
    service_id = data.get('service_id')
    talent_id = data.get('talent_id')
    service_buyer_id = data.get('service_buyer_id')
    # 参数验证
    if not service_id or not talent_id or not service_buyer_id:
        return jsonify({
            'status': 400,
            'message': '参数错误'
        })

    try:
        service_buyer = Service_buyer.query.get(service_buyer_id)
        if not service_buyer:
            return jsonify({
                "status": -1,
                "message": "交易不存在"
            })
        if service_buyer.service_id != service_id:
            return jsonify({
                "status": -2,
                "message": "交易错误"
            })
        if service_buyer.coop_talent_id:
            return jsonify({
                "status": -3,
                "message": "该服务包已确认合作"
            })
        talent = TpUser.query.get(talent_id)
        if not talent.is_online:
            return jsonify({
                "status": -4,
                "message": "该人才暂不可接服务套餐"
            })
        service_buyer.coop_talent_id = talent_id
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': '确认合作成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'message': '服务器错误'
        })


@bp.route("/finish_cooperate", methods=["POST"])
def finish_cooperate():
    data = request.json
    service_id = data.get('service_id')
    talent_id = data.get('talent_id')
    service_buyer_id = data.get('service_buyer_id')
    # 参数验证
    if not service_id or not talent_id or not service_buyer_id:
        return jsonify({
            'status': 400,
            'message': '参数错误'
        })
    try:
        service_buyer = Service_buyer.query.get(service_buyer_id)
        if not service_buyer:
            return jsonify({
                "status": -1,
                "message": "交易不存在"
            })
        if service_buyer.service_id != service_id:
            return jsonify({
                "status": -2,
                "message": "交易错误"
            })
        if not service_buyer.coop_talent_id:
            return jsonify({
                "status": -3,
                "message": "该服务包尚未确认合作"
            })
        finished_service_buyer = Finished_service_buyer(id=service_buyer.id,
                                                        service_id=service_buyer.service_id,
                                                        buyer_id=service_buyer.buyer_id,
                                                        amount=service_buyer.amount,
                                                        coop_talent_id=service_buyer.coop_talent_id,
                                                        )
        db.session.add(finished_service_buyer)
        db.session.delete(service_buyer)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': '完成合作成功'
        })
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({
            'status': 500,
            'message': '服务器错误'
        })


@bp.route("/get_talent_online", methods=["POST"])
def get_talent_online():
    data = request.json
    talent_id = data.get('talent_id')
    try:
        talent = TpUser.query.get(talent_id)
        if not talent:
            return jsonify({
                "status": -1,
                "message": "用户不存在"
            })
        return jsonify({
            'status': 200,
            "is_online": talent.is_online,
            'message': '状态获取成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'message': '服务器错误'
        })


@bp.route("/talent_online_change", methods=["POST"])
def talent_online_change():
    data = request.json
    is_online = data.get('is_online')
    talent_id = data.get('talent_id')
    try:
        talent = TpUser.query.get(talent_id)
        if not talent:
            return jsonify({
                "status": -1,
                "message": "用户不存在"
            })
        talent.is_online = is_online
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': '状态切换成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'message': '服务器错误'
        })
