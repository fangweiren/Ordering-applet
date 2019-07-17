#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webs.controllers.api import route_api
from flask import request, jsonify
from sqlalchemy import or_
from common.libs.Helper import getCurrentDate
from common.libs.UrlManager import UrlManager
from common.models.food.FoodCat import FoodCat
from common.models.food.Food import Food
from application import app, db
import requests
import json


@route_api.route("/food/index")
def foodIndex():
    resp = {"code": 200, "msg": "操作成功~", "data": {}}
    cat_list = FoodCat.query.filter_by(status=1).order_by(FoodCat.weight.desc()).all()
    data_cat_list = [{
        "id": 0,
        "name": "全部"
    }]
    if cat_list:
        for item in cat_list:
            tmp_data = {
                "id": item.id,
                "name": item.name
            }
            data_cat_list.append(tmp_data)
    resp["data"]["cat_list"] = data_cat_list

    food_list = Food.query.filter_by(status=1).order_by(Food.total_count.desc(), Food.id.desc()).limit(3).all()
    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                "id": item.id,
                "pic_url": UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)

    resp["data"]["banner_list"] = data_food_list
    return jsonify(resp)


@route_api.route("/food/search")
def foodSearch():
    resp = {"code": 200, "msg": "操作成功~", "data": {}}
    req = request.values
    cat_id = int(req["cat_id"]) if "cat_id" in req else 0
    mix_kw = str(req["mix_kw"]) if "mix_kw" in req else ""
    p = int(req["p"]) if "p" in req else 1
    query = Food.query.filter_by(status=1)

    if cat_id > 0:
        query = query.filter(Food.cat_id == cat_id)

    if mix_kw:
        rule = or_(Food.name.ilike("%{0}%".format(mix_kw)),
                   Food.tags.ilike("%{0}%".format(mix_kw)))
        query = query.filter(rule)

    if p < 1:
        p = 1
    page_size = 10
    offset = (p - 1) * page_size
    food_list = query.order_by(Food.total_count.desc(), Food.id.desc()).offset(offset).limit(page_size).all()
    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "min_price": str(item.price),
                "pic_url": UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)
    resp["data"]["food_list"] = data_food_list
    resp["data"]["has_more"] = 0 if len(data_food_list) < page_size else 1
    return jsonify(resp)
