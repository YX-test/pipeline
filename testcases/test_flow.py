#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/3 21:26
# @Author : 心蓝
import unittest
from unittestreport import ddt, list_data

from common.base_case import BaseCase
from common.test_data_handler import get_data_from_excel


@unittest.skip('我就不想让它执行')
class TestFlow(BaseCase):
    name = '投资业务流'

    def test_01register_normal_user(self):
        """
        注册普通用户
        :return:
        """
        case = {
            'title': '注册普通用户',
            'url': 'register',
            'method': 'post',
            'request_data': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v1"},'
                            '"json": {"mobile_phone":$phone$,"pwd":"12345678"}}',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}',
            'extract': '[["normal_mobile_phone", "$..mobile_phone"]]'
        }
        self.step(case)
        # 将手机号码传递给下一个测试函数
        # 可以用对象属性吗？不能
        # 绑定在类属性上
        self.__class__.normal_mobile_phone = self.case['request_data']['json']['mobile_phone']

    def test_02login_normal_user(self):
        """
        登录普通用户
        """
        case = {
            'title': '登录普通用户',
            'url': 'login',
            'method': 'post',
            'request_data': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v2"},'
                            '"json": {"mobile_phone":#normal_mobile_phone#,"pwd":"12345678"}}',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}'
        }
        self.step(case)
        # 绑定用户id，token属性
        self.__class__.normal_member_id = self.response.json()['data']['id']
        self.__class__.normal_token = self.response.json()['data']['token_info']['token']

    def test_03add_loan(self):
        """
        创建融资项目
        :return:
        """
        case = {
            'title': '添加项目',
            'url': 'add',
            'method': 'post',
            'request_data': '''
                                {
                                "headers": {"X-Lemonban-Media-Type": "lemonban.v2","Authorization":"Bearer #normal_token#"},
                                "json":{
                                "member_id":#normal_member_id#,
                                "title":"实现财富自由",
                                "amount":5000,
                                "loan_rate":18.0,
                                "loan_term":6,
                                "loan_date_type":1,
                                "bidding_days":10}
                                }
                                ''',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}'
        }
        self.step(case)
        # 绑定属性 如果通过了，绑定loan_id
        self.__class__.loan_id = self.response.json()['data']['id']

    def test_04register_admin_user(self):
        """
        注册管理员用户
        :return:
        """
        case = {
            'title': '注册管理员用户',
            'url': 'register',
            'method': 'post',
            'request_data': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v1"},'
                            '"json": {"mobile_phone":$phone$,"pwd":"12345678","type":0}}',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}'
        }
        self.step(case)
        # 保存依赖的数据 管理员手机号码
        self.__class__.admin_mobile_phone = self.case['request_data']['json']['mobile_phone']

    def test_05login_admin_user(self):
        """
        登录管理员用户
        :return:
        """
        case = {
            'title': '管理员用户登录',
            'url': 'login',
            'method': 'post',
            'request_data': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v2"},'
                            '"json": {"mobile_phone":#admin_mobile_phone#,"pwd":"12345678"}}',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}',
        }
        self.step(case)
        # 保存token
        self.__class__.admin_token = self.response.json()['data']['token_info']['token']

    def test_06audit_loan(self):
        """
        审核项目
        :return:
        """
        case = {
            'title': '审核项目',
            'url': 'audit',
            'method': 'patch',
            'request_data': '''
                                {
                                "headers": {"X-Lemonban-Media-Type": "lemonban.v2","Authorization":"Bearer #admin_token#"},
                                "json":{"loan_id":#loan_id#,"approved_or_not":true}
                                }
                                ''',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}'

        }
        self.step(case)

    def test_07register_invest_user(self):
        """
        注册投资用户
        :return:
        """
        case = {
            'title': '注册投资用户',
            'url': 'register',
            'method': 'post',
            'request_data': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v1"},'
                            '"json": {"mobile_phone":$phone$,"pwd":"12345678"}}',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}'
        }
        self.step(case)
        # 如果通过了就将电话号码保存到类属性中,共享给下一个用例
        self.__class__.invest_phone = self.case['request_data']['json']['mobile_phone']

    def test_08login_invest_user(self):
        """
        登录投资用户
        :return:
        """
        case = {
            'title': '普通投资用户登录',
            'url': 'login',
            'method': 'post',
            'request_data': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v2"},'
                            '"json": {"mobile_phone":#invest_phone#,"pwd":"12345678"}}',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}',
        }
        self.step(case)
        # 保存member_id,token
        self.__class__.invest_member_id = self.response.json()['data']['id']
        self.__class__.invest_token = self.response.json()['data']['token_info']['token']

    def test_09invest_user_recharge(self):
        """
        投资用户充值
        :return:
        """
        case = {
            'title': '普通投资用户充值',
            'url': 'recharge',
            'method': 'post',
            'request_data': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v2",'
                            '"Authorization":"Bearer #invest_token#"},'
                            '"json": {"member_id":#invest_member_id#,"amount":5000}}',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}',
        }
        self.step(case)

    def test_10invest(self):
        """
        投资
        :return:
        """
        case = {
            'title': '投资用户投资',
            'url': 'invest',
            'method': 'post',
            'request_data': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v2",'
                            '"Authorization":"Bearer #invest_token#"},'
                            '"json": {"member_id":#invest_member_id#,"loan_id":#loan_id#,"amount":5000}}',
            'status_code': 200,
            'res_type': 'json',
            'expect_data': '{"code":0,"msg":"OK"}',
        }
        self.step(case)


cases = get_data_from_excel(BaseCase.settings.TEST_DATA_FILE, 'invest_flow')


@ddt
class TestInvestFlow(BaseCase):

    name = '投资业务流'

    @list_data(cases)
    def test_invest_flow(self, case):
        self.step(case)