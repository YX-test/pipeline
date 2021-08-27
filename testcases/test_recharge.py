#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/27 21:07
# @Author : 心蓝
from unittest.mock import MagicMock

from unittestreport import ddt, list_data

from common.base_case import BaseCase
from common.fixture import register, login
from common.test_data_handler import (
    generate_no_use_phone,
    get_data_from_excel,
)


cases = get_data_from_excel(BaseCase.settings.TEST_DATA_FILE, 'recharge')


@ddt
class TestRecharge(BaseCase):
    name = '充值接口'

    @classmethod
    def setUpClass(cls) -> None:
        # 执行以下父类的方法
        super().setUpClass()
        # 1. 注册一个用户
        mobile_phone = generate_no_use_phone()
        register(mobile_phone, '12345678')

        # 2. 登录
        data = login(mobile_phone, '12345678')

        # 3. 绑定数据
        # 绑定用户的id，绑定token
        # 绑定到类属性中
        cls.member_id = data['id']
        cls.token = data['token_info']['token']

    @list_data(cases)
    def test_recharge(self, case):
        self.step(case)




