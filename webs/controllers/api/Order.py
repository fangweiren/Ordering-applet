#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webs.controllers.api import route_api
from flask import request, jsonify, g
from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.UrlManager import UrlManager
from common.libs.pay.PayService import PayService
from common.libs.pay.WeChatService import WeChatService
from common.libs.member.CartService import CartService
from application import app, db
import json
import decimal


@route_api.route("/order/info", methods=["POST"])
def orderInfo():
    resp = {"code": 200, "msg": "操作成功~", "data": {}}
    req = request.values
    params_goods = req["goods"] if "goods" in req else None
    member_info = g.member_info
    params_goods_list = []
    if params_goods:
        params_goods_list = json.loads(params_goods)

    food_dic = {}
    for item in params_goods_list:
        food_dic[item["id"]] = item["number"]

    food_ids = food_dic.keys()
    food_list = Food.query.filter(Food.id.in_(food_ids)).all()
    data_food_list = []
    yun_price = pay_price = decimal.Decimal(0.00)
    if food_list:
        for item in food_list:
            tmp_data = {
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "pic_url": UrlManager.buildImageUrl(item.main_image),
                "number": food_dic[item.id],
            }
            pay_price = pay_price + item.price * food_dic[item.id]
            data_food_list.append(tmp_data)

    default_address = {
        "name": "编程浪子",
        "mobile": "12345678901",
        "detail": "上海市浦东新区XX",
    }

    resp["data"]["food_list"] = data_food_list
    resp["data"]["pay_price"] = str(pay_price)
    resp["data"]["yun_price"] = str(yun_price)
    resp["data"]["total_price"] = str(pay_price + yun_price)
    resp["data"]["default_address"] = default_address
    return jsonify(resp)


@route_api.route("/order/create", methods=["POST"])
def orderCreate():
    resp = {"code": 200, "msg": "操作成功~", "data": {}}
    req = request.values
    type = req["type"] if "type" in req else ""
    params_goods = req["goods"] if "goods" in req else None

    items = []
    if params_goods:
        items = json.loads(params_goods)

    if len(items) < 1:
        resp["code"] = -1
        resp["msg"] = "下单失败，没有选择商品"
        return jsonify(resp)

    member_info = g.member_info
    target = PayService()
    params = {}
    resp = target.createOrder(member_info.id, items, params)

    if resp["code"] == 200 and type == "cart":
        CartService.deleteItem(member_info.id, items)

    return jsonify(resp)


@route_api.route("/order/pay", methods=["POST"])
def orderPay():
    resp = {"code": 200, "msg": "操作成功~", "data": {}}
    req = request.values
    member_info = g.member_info
    order_sn = req["order_sn"] if "order_sn" in req else ""
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        resp["code"] = -1
        resp["msg"] = "系统繁忙，请稍后重试！"
        return jsonify(resp)

    oauth_bind_info = OauthMemberBind.query.filter_by(member_id=member_info.id).first()
    if not oauth_bind_info:
        resp["code"] = -1
        resp["msg"] = "系统繁忙，请稍后重试！"
        return jsonify(resp)

    config_mina = app.config["MINA_APP"]
    notify_url = app.config["APP"]["domain"] + config_mina["callback_url"]

    target_wechat = WeChatService(merchant_key=config_mina["paykey"])
    data = {
        "appid": config_mina["appid"],
        "mch_id": config_mina["mch_id"],
        "nonce_str": target_wechat.get_nonce_str(),
        "body": "订餐",
        "out_trade_no": pay_order_info.order_sn,
        "total_price": int(pay_order_info.total_price * 100),
        "notify_url": notify_url,
        "trade_type": "JSAPI",
        "openid": oauth_bind_info.openid
    }

    pay_info = target_wechat.get_pay_info(data)

    # 保存 prepay_id 为了后面发模板消息
    pay_order_info.prepay_id = pay_info["prepay_id"]
    db.session.add(pay_order_info)
    db.session.commit()

    resp["data"]["pay_info"] = pay_info

    return jsonify(resp)
