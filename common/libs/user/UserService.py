#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import base64


class UserService:

    @staticmethod
    def geneAuthCode(user_info):
        m = hashlib.md5()
        s = "%s-%s-%s-%s" % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(s.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        s = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(s.encode("utf-8"))
        return m.hexdigest()
