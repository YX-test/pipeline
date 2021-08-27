#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/27 20:35
# @Author : 心蓝
"""
一些脚手架代码
"""
import requests

import settings
from common import logger


def register(mobile_phone, pwd, reg_name=None, _type=None):
    """
    注册用户
    :param mobile_phone:
    :param pwd:
    :param reg_name:
    :param _type:
    :return:
    """
    # 1. 构造发送注册请求的参数
    data = {
        'mobile_phone': mobile_phone,
        'pwd': pwd
    }
    if reg_name:
        data['reg_name'] = reg_name
    # 因为会传入0进来，所有不能直接if _type
    if _type is not None:
        data['type'] = _type

    headers = {"X-Lemonban-Media-Type": "lemonban.v1"}
    url = settings.INTERFACES['register']
    try:
        res = requests.post(url=url, json=data, headers=headers)
        if res.status_code == 200:
            if res.json()['code'] == 0:
                logger.info('注册用户成功')
                return res.json()['data']
        raise ValueError(res.json())
    except Exception as e:
        logger.warning('注册用户失败')
        raise e


def login(mobile_phone, pwd):
    # 1. 构造发送登录请求的参数
    data = {
        'mobile_phone': mobile_phone,
        'pwd': pwd
    }
    # v2才会返回token
    headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
    url = settings.INTERFACES['login']
    try:
        res = requests.post(url=url, json=data, headers=headers)
        if res.status_code == 200:
            if res.json()['code'] == 0:
                logger.info('登录用户成功')
                return res.json()['data']
        raise ValueError(res.json())
    except Exception as e:
        logger.warning('登录用户失败')
        raise e


def add_loan(member_id, token, title='借钱实现财富自由', amount=5000, loan_rate=12.0,
             loan_term=3, loan_date_type=1, bidding_days=5):
    """
    添加一个项目
    :param member_id:
    :param token:
    :param title:
    :param amount:
    :param loan_rate:
    :param loan_term:
    :param loan_date_type:
    :param bidding_days:
    :return:
    """
    # 1. 构造发送登录请求的参数
    data = {
        'member_id': member_id,
        'title': title,
        'amount': amount,
        'loan_rate': loan_rate,
        'loan_term': loan_term,
        'loan_date_type': loan_date_type,
        'bidding_days': bidding_days
    }
    # 需要鉴权
    headers = {"X-Lemonban-Media-Type": "lemonban.v2", 'Authorization': 'Bearer {}'.format(token)}
    url = settings.INTERFACES['add']
    try:
        res = requests.post(url=url, json=data, headers=headers)
        if res.status_code == 200:
            if res.json()['code'] == 0:
                logger.info('创建项目成功')
                return res.json()['data']
        raise ValueError(res.json())
    except Exception as e:
        logger.warning('登录用户失败')
        raise e


if __name__ == '__main__':
    from common.test_data_handler import generate_no_use_phone
    phone = generate_no_use_phone()
    register(phone, '12345678', _type=0)
    res = login(phone, '12345678')
    token = res['token_info']['token']
    member_id = res['id']
    loan = add_loan(member_id, token)
    print(loan)
