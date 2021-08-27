#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/3 20:08
# @Author : 心蓝
import json
import unittest

import requests
from jsonpath import jsonpath

import settings
from common import db, logger
from common.make_requests import send_http_request
from common.test_data_handler import (
    generate_no_use_phone,
    replace_args_by_re)


class BaseCase(unittest.TestCase):
    """
    测试基类
    """
    # 将公用模块绑定到类属性上
    db = db
    logger = logger
    settings = settings
    name = 'base接口'
    session = requests.session()

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info('========= {} 开始测试 ======='.format(cls.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.logger.info('========= {} 测试结束 ======='.format(cls.name))

    def step(self, case):
        """
        测试步骤
        :param case:
        :return:
        """

        self.logger.info('********** 用例【{}】 开始执行 *************'.format(case['title']))
        # 绑定case到对象属性上便于其他对象方法访问
        self.case = case
        # 1. 处理测试数据
        self.__process_test_data()
        # 2. 发送请求
        self.send_http_request()
        # 3. 断言
        self.__assert_res()
        # 4. 提取依赖数据
        self.__extract_data()
        self.logger.info('********** 用例【{}】 测试成功 *************'.format(case['title']))

    def generate_test_data(self):
        """
        动态生成测试数据 phone
        :return:
        """
        # 子类可以复写实现自定义的生成测试数据
        # 1 生成动态数据并替换
        try:
            if '$phone$' in self.case['request_data']:
                # 如果request_data中存在生成数据的标志
                phone = generate_no_use_phone()
                # 立刻替换
                self.case['request_data'] = self.case['request_data'].replace('$phone$', phone)
                if self.case.get('sql'):
                    self.case['sql'] = self.case['sql'].replace('#phone#', phone)
        except Exception as e:
            self.logger.warning('用例【{}】生成测试数据$phone$的时候失败'.format(self.case['title']))
            raise e

    def __process_url(self):
        """
        url的处理
        :return:
        """
        try:
            if 'http' in self.case['url']:
                # 全地址
                pass
            elif '/' in self.case['url']:
                self.case['url'] = self.settings.PROJECT_HOST + self.case['url']
            else:
                self.case['url'] = self.settings.INTERFACES[self.case['url']]
        except Exception as e:
            self.logger.warning('用例【{}】在拼接处理url的时候失败'.format(self.case['title']))
            raise e

    def __replace_args(self):
        """
        替换参数
        :return:
        """
        try:
            self.case['url'] = replace_args_by_re(self.case['url'], self)
            self.case['request_data'] = replace_args_by_re(self.case['request_data'], self)
            # sql也需要替换
            if self.case.get('sql'):
                self.case['sql'] = replace_args_by_re(self.case['sql'], self)
        except Exception as e:
            self.logger.warning('用例【{}】替换参数时失败'.format(self.case['title']))
            raise e

    def __process_test_data(self):
        """
        处理测试数据
        :return:
        """

        # 1. 生成测试数据
        self.generate_test_data()
        # 2. url处理
        self.__process_url()
        # 3. 替换依赖参数
        self.__replace_args()

        # 4. 将请求数据和期望数据转换为python对象
        try:
            self.case['request_data'] = json.loads(self.case['request_data'])
            self.case['expect_data'] = json.loads(self.case['expect_data'])
        except Exception as e:
            self.logger.warning('用例【{}】在请求参数反序列化时失败'.format(self.case['title']))
            raise e

    def send_http_request(self):
        """
        发送http请求
        :return:
        """
        # 2. 发送请求
        # 根据测试用例数据来发送请求
        try:
            self.response = self.send_http_request_by_session(
                self.case['url'],
                self.case['method'],
                **self.case['request_data']
            )
        except Exception as e:
            self.logger.warning('用例【{}】在发送请求时失败'.format(self.case['title']))
            raise e

    def send_http_request_by_session(self, url, method, **kwargs) -> requests.Response:
        """
        发送http请求自动处理cookie信息
        :param url:
        :param method:
        :param kwargs:
        :return:
        """
        method = method.lower()
        return getattr(self.session, method)(url=url, **kwargs)

    def __assert_status_code(self):
        """
        响应状态码断言
        :return:
        """
        try:
            self.assertEqual(self.case['status_code'], self.response.status_code)
        except AssertionError as e:
            self.logger.warning('用例【{}】响应状态码断言失败'.format(self.case['title']))
            raise e
        else:
            self.logger.info('用例【{}】响应状态码断言成功'.format(self.case['title']))

    def assert_response(self):
        """
        断言响应数据
        :return:
        """
        if self.case.get('res_type') == 'json':
            res = self.response.json()
        elif self.case.get('res_type') == 'xml':
            pass
        elif self.case.get('res_type') == 'html':
            pass

        try:
            self.assertEqual(self.case['expect_data'], {'code': res['code'], 'msg': res['msg']})
        except AssertionError as e:
            self.logger.warning('用例【{}】响应数据断言失败'.format(self.case['title']))
            self.logger.info('用例【{}】期望的结果是{}'.format(self.case['title'], self.case['expect_data']))
            self.logger.info('用例【{}】返回数据是{}'.format(self.case['title'], res))
            raise e
        else:
            self.logger.info('用例【{}】响应数据断言成功'.format(self.case['title']))

    def assert_db(self):
        """
        数据库断言
        :return:
        """
        if self.case.get('sql'):
            sqls = self.case['sql'].split(',')
            for sql in sqls:
                self.logger.info('用例【{}】数据校验的sql为:{}'.format(self.case['title'], sql))
                try:
                    self.assertTrue(self.db.exist(sql))
                except AssertionError as e:
                    self.logger.warning('用例【{}】数据库断言失败'.format(self.case['title']))
                    raise e
                except Exception as e:
                    self.logger.warning('用例【{}】数据库查询失败'.format(self.case['title']))
                    raise e
                else:
                    self.logger.info('用例【{}】数据断言成功'.format(self.case['title']))

    def __extract_data_from_json(self):
        """
        根据jsonpath从json数据中提取数据并保存到对应的类属性中
        :return:
        """
        try:
            # 将提取规则json数组转换成列表
            rules = json.loads(self.case['extract'])
        except Exception as e:
            raise ValueError('用例【{}】的extract字段数据:{}格式不正确'.format(self.case['title'], self.case['extract']))
        for rule in rules:
            # 循环获取每个规则
            name = rule[0]   # 要绑定的属性名
            exp = rule[1]    # jsonpath 表达式
            value = jsonpath(self.response.json(), exp)  # 在响应数据中去提取数据
            if value:  # 注意：如果提取到了值是一个列表格式
                # 如果提取到了数据就绑定到类属性中
                setattr(self.__class__, name, value[0])  #
            else:
                raise ValueError('用例【{}】的提取表达式{}提取不到数据'.format(self.case['title'], self.case['extract']))

    def __extract_data(self):
        """
        从响应中提取数据并保存到对应的类属性中
        :return:
        """
        # 1. 判断是否需要提取
        if self.case.get('extract'):
            if self.case['res_type'].lower() == 'json':
                self.__extract_data_from_json()
            elif self.case['res_type'].lower() == 'html':
                raise ValueError('还没有实现html数据的提取')
            elif self.case['res_type'].lower() == 'xml':
                raise ValueError('还没有实现xml数据的提取')
            else:
                raise ValueError('请填写正确的res_type')

    def __assert_res(self):
        """
        断言
        :return:
        """
        # 3. 断言
        # 3.1 断言响应状态码
        self.__assert_status_code()

        # 3.2 响应结果断言
        # 判断响应数据类型
        self.assert_response()

        # 3.3 数据库断言
        self.assert_db()

