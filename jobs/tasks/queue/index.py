#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import datetime
from common.models.queue.QueueList import QueueList
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.food.Food import Food
from common.models.food.FoodSaleChangeLog import FoodSaleChangeLog
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentDate
from common.libs.pay.WeChatService import WeChatService
from application import app, db
from sqlalchemy import func

'''
python manage.py runjob -m queue/index
'''


class JobTask:
    def __init__(self):
        pass

    def run(self, params):
        list = QueueList.query.filter_by(status=-1).order_by(QueueList.id.asc()).limit(1).all()
        for item in list:
            if item.queue_name == "pay":
                self.handlePay(item)

            item.status = 1
            item.updated_time = getCurrentDate()
            db.session.add(item)
            db.session.commit()

    def handlePay(self, item):
        data = json.loads(item.data)
        if "member_id" not in data or "pay_order_id" not in data:
            return False

        oauth_bind_info = OauthMemberBind.query.filter_by(member_id=data["member_id"]).first()
        if not oauth_bind_info:
            return False

        pay_order_info = PayOrder.query.filter_by(id=data["pay_order_id"]).first()
        if not pay_order_info:
            return False

        pay_order_items = PayOrderItem.query.fitter_by(pay_order_id=pay_order_info.id).all()
        notice_content = []
        # 更新销售数量
        if pay_order_items:
            date_from = datetime.datetime.now().strftime("%Y-%M-01 00:00:00")
            date_to = datetime.datetime.now().strftime("%Y-%M-31 23:59:59")
            for item in pay_order_items:
                tmp_food_info = Food.query.filter_by(id=item.food_id).first()
                if not tmp_food_info:
                    continue

                notice_content.append("%s %s份" % (tmp_food_info.name, item.quantity))

                # 当月的销售
                tmp_stat_info = db.session.query(FoodSaleChangeLog, func.sum(FoodSaleChangeLog.quantity).label("total")) \
                    .filter(FoodSaleChangeLog.food_id == item.food_id) \
                    .filter(FoodSaleChangeLog.created_time >= date_from,
                            FoodSaleChangeLog.created_time <= date_to).first()
                tmp_month_count = tmp_stat_info[1] if tmp_stat_info[1] else 0
                tmp_food_info.total_count += 1
                tmp_food_info.month_count = tmp_month_count
                db.session.add(tmp_food_info)
                db.session.commit()

        keyword1_val = pay_order_info.note if pay_order_info.note else "无"
        keyword2_val = "、".join(notice_content)
        keyword3_val = str(pay_order_info.total_price)
        keyword4_val = str(pay_order_info.order_number)
        keyword5_val = ""

        target_wechat = WeChatService()
        access_token = target_wechat.getAccessToken()
        headers = {"Content-Type": "application/json"}
        url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s" % access_token

        params = {
            "touser": oauth_bind_info.openid,
            "template_id": "7_a2OIu9QJ5dkYjA6HIU5i7FOFKM9nqpgoWCw0qmaqA",
            "page": "pages/my/order_list",
            "form_id": pay_order_info.prepay_id,
            "data": {
                "keyword1": {
                    "value": keyword1_val
                },
                "keyword2": {
                    "value": keyword2_val
                },
                "keyword3": {
                    "value": keyword3_val
                },
                "keyword4": {
                    "value": keyword4_val
                },
                "keyword5": {
                    "value": keyword5_val
                }
            }
        }

        r = requests.post(url=url, data=json.dumps(params), headers=headers)
        r.encoding = "utf-8"
        app.logger.info(r.text)
        return True
