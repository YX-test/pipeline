#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/20 20:06
# @Author : 心蓝
import unittest

from unittestreport import TestRunner

import settings


if __name__ == '__main__':
    # 1. 收集用例
    ts = unittest.defaultTestLoader.discover(settings.TESTCASES_DIR)
    # 2. 运行并生成测试报告

    TestRunner(ts, **settings.REPORT_CONFIG).run()




