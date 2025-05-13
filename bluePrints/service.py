import base64
import os, oss2
import time
from flask import Blueprint, request, jsonify, session
from sqlalchemy import and_, or_
from hooks import *
from config import *
from models import TpUser

bp = Blueprint("service", __name__, url_prefix="/service")


@bp.route("/get_all_services", methods=["POST"])
def get_all_services():
    services = ServicePkg.query.all()
    services = [service.to_json() for service in services]
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
            features=ServicePkg.concatenate_features(data.get('features'))
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
        users = TpUser.query.filter(TpUser.mobile.like(f"%{phone}%")).all()

        if not users:
            return jsonify({
                "status": 404,
                "message": "未找到用户"
            })

        users = [{
            "id": user.user_id,
            "name": user.realname,
            "phone": user.mobile
        } for user in users]

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


# TODO
# @bp.route("/assign_talent", methods=["POST"])
# def assign_talent():
#     """
#     分配人才接口
#     请求参数:
#     - service_id: 服务包ID
#     - talent_id: 人才ID
#     """
#     # 获取请求参数
#     data = request.json
#     service_id = data.get('service_id')
#     talent_id = data.get('talent_id')
#     # 参数验证
#     if not service_id or not talent_id:
#         return jsonify({
#             'status': 400,
#             'message': '参数错误'
#         })
#
#     try:
#
#         return jsonify({
#             'status': 200,
#             'message': '分配成功'
#         })
#
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({
#             'status': 500,
#             'message': '服务器错误'
#         })