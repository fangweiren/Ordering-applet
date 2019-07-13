#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import app

"""
统计拦截器
"""
from webs.interceptors.Authinterceptor import *
from webs.interceptors.Errorinterceptor import *

"""
蓝图功能，对所有的 url 进行蓝图功能配置
"""
from webs.controllers.index import route_index
from webs.controllers.static import route_static
from webs.controllers.user.User import route_user
from webs.controllers.account.Account import route_account
from webs.controllers.finance.Finance import route_finance
from webs.controllers.food.Food import route_food
from webs.controllers.member.Member import route_member
from webs.controllers.stat.Stat import route_stat
from webs.controllers.api import route_api
from webs.controllers.upload.Upload import route_upload

app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_static, url_prefix="/static")
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_account, url_prefix="/account")
app.register_blueprint(route_finance, url_prefix="/finance")
app.register_blueprint(route_food, url_prefix="/food")
app.register_blueprint(route_member, url_prefix="/member")
app.register_blueprint(route_stat, url_prefix="/stat")
app.register_blueprint(route_api, url_prefix="/api")
app.register_blueprint(route_upload, url_prefix="/upload")
