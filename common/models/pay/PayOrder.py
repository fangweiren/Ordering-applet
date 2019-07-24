#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, Numeric, String, Text
from sqlalchemy.schema import FetchedValue
from application import db


class PayOrder(db.Model):
    __tablename__ = 'pay_order'
    __table_args__ = (
        db.Index('idx_member_id_status', 'member_id', 'status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(40), nullable=False, unique=True, server_default=db.FetchedValue())
    member_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    total_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    yun_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    pay_price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    pay_sn = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())
    prepay_id = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())
    note = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_address_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    express_info = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    comment_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    pay_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
