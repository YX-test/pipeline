#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/10 20:19
# @Author : 心蓝
import unittest

from unittestreport import ddt, list_data

from common.base_case import BaseCase


cases = [
    {'title': '课堂派登录',
     'method': 'post',
     'url': 'https://v4.ketangpai.com/UserApi/login',
     'request_data': '{"data": {"email": "877649301@qq.com", "password": "Pythonxinlan", "remember": 0}}',
     'status_code': 200,
     'res_type': 'json',
     'expect_data': '{"status": 1}'
     },
    {'title': '获取所有课程信息',
     'method': 'get',
     'url': 'https://v4.ketangpai.com/CourseApi/lists',
     'request_data': '{}',
     'status_code': 200,
     'res_type': 'json',
     'expect_data': '{"status": 1}'
     },
]


@ddt
class TestCourseFlow(BaseCase):
    name = '课堂派业务流'

    @list_data(cases)
    def test_course(self, case):
        self.step(case)

    def assert_response(self):
        """
        复写这个方法
        :return:
        """
        if self.case.get('res_type') == 'json':
            res = self.response.json()
        elif self.case.get('res_type') == 'xml':
            pass
        elif self.case.get('res_type') == 'html':
            pass

        try:
            self.assertEqual(self.case['expect_data'], {'status': res['status']})
        except AssertionError as e:
            self.logger.warning('用例【{}】响应数据断言失败'.format(self.case['title']))
            self.logger.info('用例【{}】期望的结果是{}'.format(self.case['title'], self.case['expect_data']))
            self.logger.info('用例【{}】返回数据是{}'.format(self.case['title'], res))
            raise e
        else:
            self.logger.info('用例【{}】响应数据断言成功'.format(self.case['title']))

if __name__ == '__main__':
    unittest.main