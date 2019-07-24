#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

route_api = Blueprint("api_page", __name__)
from webs.controllers.api.Member import *
from webs.controllers.api.Food import *
from webs.controllers.api.Cart import *
from webs.controllers.api.Order import *
from webs.controllers.api.My import *


@route_api.route("/")
def index():
    return "Mina Api V1.0~~"
