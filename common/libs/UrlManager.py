#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import application


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        release_version = application.app.config.get("RELEASE_VERSION")
        ver = "%s" % (int(time.time())) if not release_version else release_version
        path = "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl(path)

    @staticmethod
    def buildImageUrl(path):
        url = application.app.config.get("APP")["domain"] + application.app.config.get("UPLOAD")["prefix_url"] + path
        return url
