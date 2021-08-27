#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/20 20:06
# @Author : 心蓝
import datetime
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 项目主机
PROJECT_HOST = 'http://api.lemonban.com/futureloan'

# 服务器公钥
SERVER_RSA_PUB_KEY = """
    -----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQENQujkLfZfc5Tu9Z1LprzedE
    O3F7gs+7bzrgPsMl29LX8UoPYvIG8C604CprBQ4FkfnJpnhWu2lvUB0WZyLq6sBr
    tuPorOc42+gLnFfyhJAwdZB6SqWfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGo8Dg+S
    kKlZFc8Br7SHtbL2tQIDAQAB
    -----END PUBLIC KEY-----
    """

# 接口地址
INTERFACES = {
    # =================== 用户模块 =========================
    'register': PROJECT_HOST + '/member/register',
    'login': PROJECT_HOST + '/member/login',
    'recharge': PROJECT_HOST + '/member/recharge',
    'invest': PROJECT_HOST + '/member/invest',
    # =================== 项目模块 =========================
    'add': PROJECT_HOST + '/loan/add',
    'audit': PROJECT_HOST + '/loan/audit'
}



# 日志配置
LOG_CONFIG = {
    'name': 'py41',
    'filename': os.path.join(BASE_DIR, 'logs', 'py41.log'),
    # 'encoding': 'utf-8',
    # 'fmt': None,
    # 'when': 'd',
    # 'interval': 1,
    # 'backup_count': 7,
    'debug': True
}

# 测试数据
TEST_DATA_FILE = os.path.join(BASE_DIR, 'test_data', 'testcases.xlsx')

# 测试用例目录
TESTCASES_DIR = os.path.join(BASE_DIR, 'testcases')

# 测试报告
REPORT_CONFIG = {
    'filename': '{}_py41接口自动化测试报告.html'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')),
    'report_dir': os.path.join(BASE_DIR, 'reports'),
    'title': 'py41接口自动化测试报告',
    'tester': '心蓝',
    'desc': "借钱是快靠不住的",
    # templates=1
}

# 数据库配置
DB_CONFIG = {
    'engine': 'mysql',  # 指定数据库引擎,
    'host': 'api.lemonban.com',    #  主机
    'user': 'future',              # 用户名
    'password': '123456',          # 密码
    'db': 'futureloan',            # 数据库
    'port': 3306,                  # 端口
    'charset': 'utf8',             # 字符串编码
    'autocommit': True
}
