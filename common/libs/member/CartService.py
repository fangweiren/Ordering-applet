#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common.models.member.MemberCart import MemberCart
from common.libs.Helper import getCurrentDate
from application import db


class CartService:

    @staticmethod
    def setItems(member_id=0, food_id=0, number=0):
        if member_id < 1 or food_id < 1 or number < 1:
            return False

        cart_info = MemberCart.query.filter_by(member_id=member_id, food_id=food_id).first()
        if cart_info:
            model_cart = cart_info
        else:
            model_cart = MemberCart()
            model_cart.member_id = member_id
            model_cart.food_id = food_id
            model_cart.created_time = getCurrentDate()

        model_cart.quantity = number
        model_cart.updated_time = getCurrentDate()
        db.session.add(model_cart)
        db.session.commit()
        return True
