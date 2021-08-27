#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/20 21:46
# @Author : 心蓝
"""

1. 输入参数 url, method, 以及需要携带的各种类型的http请求参数和请求头等
2. 可以使用动态关键字参数解决第一个步参数过的问题
3. 使用requests库请求方法的同名参数便于传递
4. 根据传入的method，发送对应的请求
"""
import requests


def send_http_request(url, method='get', **kwargs):
    """
    发送http请求
    :param url:
    :param method:
    :param kwargs: 接受requests库原生请求方法的关键字参数
    :return:
    """
    # 为了防止用户传入的方法名的大小写格式问题
    # 统一一下大小写格式
    method = method.lower()
    # 根据方法名发送对应的请求
    return getattr(requests, method)(url, **kwargs)

    # kwargs = {'json': {'mobile_phone': '111111'}}
    # if method == 'get':
    #     res = requests.get(url, **kwargs)  # =》requests.get(url, json={'mobile_phone': '111111'})
    # elif method == 'post':
    #     res = requests.post(url, **kwargs)
    # elif method == 'put':
    #     res = requests.put(url, **kwargs)
    # elif method == 'patch':
    #     res = requests.patch(url, **kwargs)
    # elif method == 'delete':
    #     res = requests.delete(url, **kwargs)
    # else:
    #     raise ValueError('请输入正确的请求方法！')
    # return res


if __name__ == '__main__':

    send_http_request('', 'post', json={'mobile_phone': '111111'})