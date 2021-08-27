#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/31 20:39
# @Author : 心蓝
from unittestreport import ddt, list_data

from common.base_case import BaseCase

from common.fixture import register, login, add_loan
from common.test_data_handler import (
    generate_no_use_phone, get_data_from_excel)


cases = get_data_from_excel(BaseCase.settings.TEST_DATA_FILE, 'audit')


@ddt
class TestAudit(BaseCase):
    name = '审核接口'

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # 1. 注册一个不同用户
        mobile_phone = generate_no_use_phone()
        pwd = '12345678'
        register(mobile_phone, pwd)
        # 2. 登录普通用户
        data = login(mobile_phone, pwd)
        # 3. 保存需要的数据
        # 保存融资用户的member_id和token
        cls.normal_member_id = data['id']
        cls.normal_token = data['token_info']['token']
        # 4. 注册管理员用户
        mobile_phone = generate_no_use_phone()
        register(mobile_phone, pwd, _type=0)
        # 5. 登录管理员用户
        data = login(mobile_phone, pwd)
        # 6. 保存需要的数据
        # 保存管理员用户的token
        cls.token = data['token_info']['token']

    def setUp(self) -> None:
        # 1. 创建一个项目
        data = add_loan(self.normal_member_id, self.normal_token)
        # 2. 保存新的项目的id
        # 通过对象属性保存项目id
        self.loan_id = data['id']

    @list_data(cases)
    def test_audit(self, case):
        self.step(case)