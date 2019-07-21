#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webs.controllers.api import route_api
from flask import request, jsonify, g
from common.models.food.Food import Food
from common.libs.member.CartService import CartService


@route_api.route("/cart/set", methods=["POST"])
def cartSet():
    resp = {"code": 200, "msg": "操作成功~", "data": {}}
    req = request.values
    food_id = int(req["id"]) if "id" in req else 0
    number = int(req["number"]) if "number" in req else 0
    if food_id < 1 or number < 1:
        resp["code"] = -1
        resp["msg"] = "添加购物车失败-1"
        return jsonify(resp)

    member_info = g.member_info
    if not member_info:
        resp["code"] = -1
        resp["msg"] = "添加购物车失败-2"
        return jsonify(resp)

    food_info = Food.query.filter_by(id=food_id).first()
    if not food_info:
        resp["code"] = -1
        resp["msg"] = "添加购物车失败-3"
        return jsonify(resp)

    if food_info.stock < number:
        resp["code"] = -1
        resp["msg"] = "添加购物车失败，库存不足"
        return jsonify(resp)

    ret = CartService.setItems(member_id=member_info.id, food_id=food_id, number=number)
    if not ret:
        resp["code"] = -1
        resp["msg"] = "添加购物车失败-4"
        return jsonify(resp)

    return jsonify(resp)
