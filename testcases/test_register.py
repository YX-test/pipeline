#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/20 21:21
# @Author : 心蓝

from unittestreport import ddt, list_data

from common.test_data_handler import get_data_from_excel
from common.base_case import BaseCase

cases = get_data_from_excel(BaseCase.settings.TEST_DATA_FILE, 'register')


@ddt
class RegisterTestCase(BaseCase):
    name = '注册接口'

    @list_data(cases)
    def test_register(self, case):

        self.step(case)


if __name__ == '__main__':
    import unittest
    unittest.main()