#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/7 21:24
# @Author : 心蓝
from unittestreport import ddt, list_data

from common.base_case import BaseCase
from common.test_data_handler import get_data_from_excel
from common.encrypt_handler import generate_sign

cases = get_data_from_excel(BaseCase.settings.TEST_DATA_FILE, 'invest')


@ddt
class TestInvest(BaseCase):
    name = '投资接口'

    @list_data(cases)
    def test_invest(self, case):
        self.step(case)

    def send_http_request(self):
        """
        复写父类方法实现v3版本鉴权
        :return:
        """
        if self.case['request_data']['headers']['X-Lemonban-Media-Type'] == 'lemonban.v3':
            # 获取token
            token = self.case['request_data']['headers']['Authorization'].split(' ')[-1]
            # 生成签名
            sign, timestamp = generate_sign(token, self.settings.SERVER_RSA_PUB_KEY)
            # 添加到参数中去
            self.case['request_data']['json']['sign'] = sign
            self.case['request_data']['json']['timestamp'] = timestamp

        super().send_http_request()
