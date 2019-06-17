#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application import app
from webs.controllers.index import route_index

app.register_blueprint(route_index, url_prefix="/")
