#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webs.controllers.api import route_api
from flask import request, jsonify
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
    return
