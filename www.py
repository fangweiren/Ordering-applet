#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import app
from webs.controllers.index import route_index
from webs.controllers.static import route_static
from webs.controllers.user.User import route_user
from webs.controllers.account.Account import route_account

app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_static, url_prefix="/static")
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_account, url_prefix="/account")
