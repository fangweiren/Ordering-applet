#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import app
from flask import request, redirect, g
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.LogService import LogService
import re


@app.before_request
def before_request():
    ignore_urls = app.config["IGNORE_URLS"]
    ignore__check_login_urls = app.config["IGNORE_CHECK_LOGIN_URLS"]
    path = request.path

    pattern = re.compile("%s" % "|".join(ignore__check_login_urls))
    if pattern.match(path):
        return

    if "/api" in path:
        return

    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info

    # 加入日志
    LogService.addAccessLog()

    pattern = re.compile("%s" % "|".join(ignore_urls))
    if pattern.match(path):
        return

    if not user_info:
        return redirect(UrlManager.buildUrl("/user/login"))

    return


def check_login():
    """
    判断用户是否已经登录
    """
    cookies = request.cookies
    auth_cookie = cookies[app.config["AUTH_COOKIE_NAME"]] if app.config["AUTH_COOKIE_NAME"] in cookies else None
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    if user_info.status != 1:
        return False

    return user_info
