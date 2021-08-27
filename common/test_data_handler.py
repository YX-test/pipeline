#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/17 16:35
# @Author : 心蓝
import json
import re
import random

from jsonpath import  jsonpath

from openpyxl import load_workbook
from common import db


def get_data_from_excel(file, sheet_name=None):
    """
    获取Excel文件中的测试数据
    """
    # 1. 读取excel文件
    wb = load_workbook(file)

    # 2. 读取对应的表
    if sheet_name is None:
        ws = wb.active
    else:
        ws = wb[sheet_name]
    # 3. 创建一个列表容器存放数据
    data = []
    # 4. 获取表头头
    row_list = list(ws.rows)
    title = [item.value for item in row_list[0]]
    # 5. 获取其他数据
    for row in row_list[1:]:
        # 获取每一个行数据
        temp = [i.value for i in row]
        # 将表头与这一行数据打包，转换成字典
        data.append(dict(zip(title, temp)))

    return data


def generate_phone():
    """
    随机的生成手机号码
    :return:
    """
    # 1开头
    # 11位
    # 第二个数字是3-9

    # phone = ['1', str(random.randint(3, 9))]
    phone = ['158']
    for i in range(8):
        phone.append(str(random.randint(0, 9)))
    return ''.join(phone)


def generate_no_use_phone(sql="select id from member where mobile_phone='{}'"):
    """
    生成没有注册的手机号码
    :return:
    """
    while True:
        phone = generate_phone()

        if not db.exist(sql.format(phone)):
            return phone


def replace_args_by_re(s, obj):
    """
    通过正则表达式动态替换参数
    :param s: 需要被替换的参数字符串
    :param obj: 提供数据的对象
    :return:
    """
    # 1. 先找出字符串中的槽位
    args = re.findall('#(.*?)#', s)
    # 2. 循环参数
    for arg in args:
        # 3. 获取obj对应参数名的属性
        value = getattr(obj, arg, None)
        # 4. 替换
        if value:
            s = s.replace('#{}#'.format(arg), str(value))
    return s


def extract_data(rule, json_data, obj):
    """
    根据提取表达式提取响应数据中的值并绑定到obj的对应属性上
    :param rule: 提取规则
    :param json_data:
    :param obj:
    :return:
    """
    data = json.loads(json_data)

    name = rule[0]  # 要绑定的属性名
    exp = rule[1]  # jsonpath 表达式
    value = jsonpath(data, exp)  # 在响应数据中去提取数据
    if value:
        # 如果提取到了数据就绑定到类属性中
        setattr(obj, name, value[0])
    else:
        raise ValueError('用例的提取表达式{}提取不到数据'.format(rule))


if __name__ == '__main__':
    rule = ["normal_mobile_phone", "$..mobile_phone"]

    class A:
        pass

    data = '{"mobile_phone": "15873061798","pwd": "123456"}'

    extract_data(rule, data, A)
    print(A.normal_mobile_phone)
#     s = '''{
# "headers": {"X-Lemonban-Media-Type": "lemonban.v2","Authorization":"Bearer #aaa#"},
# "json":{"loan_id":#bbb#,"approved_or_not":true}
# }'''
#     class A:
#         pass
#     A.token = '我是token'
#     A.loan_id = 8888
#     res = replace_args_by_re(s, A)
#     print(res)
    # res = get_data_from_excel(r'D:\project\classes\py41\day23\test_data\testcases.xlsx', 'register')
    # print(res)
    # print(generate_phone())
    # print(generate_no_use_phone())