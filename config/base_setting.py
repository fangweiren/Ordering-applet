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

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除",
}
