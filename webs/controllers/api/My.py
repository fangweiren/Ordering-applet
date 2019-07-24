#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webs.controllers.api import route_api
from flask import request, jsonify, g
from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.libs.Helper import selectFilterObj, getDictFilterField
from common.libs.UrlManager import UrlManager


@route_api.route("/my/order")
def myOrderList():
    resp = {"code": 200, "msg": "操作成功~", "data": {}}
    req = request.values
    member_info = g.member_info

    status = int(req["status"]) if "status" in req else 0
    query = PayOrder.query.filter_by(member_id=member_info.id)

    if status == -8:  # 待付款
        query = query.filter(PayOrder.status == -8)
    elif status == -7:  # 待发货
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == -7, PayOrder.comment_status == 0)
    elif status == -6:  # 待收货
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == -6, PayOrder.comment_status == 0)
    elif status == -5:  # 待评价
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1, PayOrder.comment_status == 0)
    elif status == 1:  # 已评价
        query = query.filter(PayOrder.status == 1, PayOrder.express_status == 1, PayOrder.comment_status == 1)
    else:  # 已关闭
        query = query.filter(PayOrder.status == 0)

    pay_order_list = query.order_by(PayOrder.id.desc()).all()
    data_pay_order_list = []
    if pay_order_list:
        pay_order_ids = selectFilterObj(pay_order_list, "id")
        pay_order_item_list = PayOrderItem.query.filter(PayOrderItem.pay_order_id.in_(pay_order_ids)).all()
        food_ids = selectFilterObj(pay_order_item_list, "food_id")
        food_map = getDictFilterField(Food, Food.id, "id", food_ids)
        pay_order_item_map = {}

        if pay_order_item_list:
            for item in pay_order_item_list:
                if item.pay_order_id not in pay_order_item_map:
                    pay_order_item_map[item.pay_order_id] = []

                tmp_food_info = food_map[item.food_id]
                pay_order_item_map[item.pay_order_id].append({
                    "id": item.id,
                    "food_id": item.food_id,
                    "quantity": item.quantity,
                    'price':str( item.price ),
                    "pic_url": UrlManager.buildImageUrl(tmp_food_info.main_image),
                    "name": tmp_food_info.name,
                })

        for item in pay_order_list:
            tmp_data = {
                "status": item.pay_status,
                "status_desc": item.status_desc,
                "date": item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "order_number": item.order_number,
                "note": item.note,
                "total_price": str(item.total_price),
                "goods_list": pay_order_item_map[item.id]
            }

            data_pay_order_list.append(tmp_data)

    resp["data"]["pay_order_list"] = data_pay_order_list
    return jsonify(resp)
