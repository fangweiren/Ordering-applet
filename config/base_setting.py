#!/usr/bin/env python
# -*- coding: utf-8 -*-
SERVER_PORT = 9000
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = "nancy_food"

# 过滤 url
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

API_IGNORE_URLS = [
    "^/api"
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除",
}

MINA_APP = {
    "appid": "wx759d38ee4da2062d",
    "appkey": "fd6661994ed89a5d79d8d6f6999d2931",
    "paykey": "xxxxxxxxxxxxxx换自己的",
    "mch_id": "xxxxxxxxxxxx换自己的",
    "callback_url": "/api/order/callback"
}

UPLOAD = {
    "ext": ["jpg", "gif", "bmp", "jpeg", "png"],
    "prefix_path": "/webs/static/upload/",
    "prefix_url": "/static/upload/"
}

APP = {
    "domain": "http://192.168.37.133:9000"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "订单关闭",
    "1": "支付成功",
    "-8": "待支付",
    "-7": "待发货",
    "-6": "待收货",
    "-5": "待评价",
}
