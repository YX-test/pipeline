#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/20 21:03
# @Author : 心蓝
# python中的每一个包下都会有一个__init__.py文件

# 当包被导入的时候，这个__init__.py文件里的代码会被执行，并且只会执行一遍
import unittest
import settings
from common.log_handler import get_logger
from common.db_handler import SQLdbHandler

logger = get_logger(**settings.LOG_CONFIG)
db = SQLdbHandler(settings.DB_CONFIG)

