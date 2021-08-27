#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/7 20:35
# @Author : 心蓝
import base64
import time

import rsa


def rsa_encrypt(msg: str, server_pub_key: str):
    """
    公钥加密
    :param msg: 需要加密的信息
    :param server_pub_key: pem格式的公钥
    :return:
    """
    # 1. 获取公钥对象
    # 转换成字节码
    pub_key_byte = server_pub_key.encode()
    pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_byte)

    # 2. 将加密数据转换成字节
    content = msg.encode('utf-8')

    # 3. 加密
    crypt_msg = rsa.encrypt(content, pub_key)
    # 4. 将加密的结果字节转化成base64编码的字符串
    res = base64.b64encode(crypt_msg).decode()
    return res


def generate_sign(token, pub_key: str):
    """
    生成签名
    :param token: token字符串
    :param pub_key: pem格式的公钥
    :return:
    """
    # 1. 获取token的前50位
    token_50 = token[:50]

    # 2. 生成时间戳
    timestamp = int(time.time())

    # 3. 拼接token前50位和时间戳
    msg = token_50 + str(timestamp)

    # 4. RSA加密
    sign = rsa_encrypt(msg, pub_key)

    return sign, timestamp


if __name__ == '__main__':

    import settings
    from common.make_requests import send_http_request
    from common.test_data_handler import generate_no_use_phone
    from common.fixture import login, register
    mobile_phone = generate_no_use_phone()
    pwd = '12345678'
    # 1. 注册
    register(mobile_phone, pwd)
    # 2. 登录
    res = login(mobile_phone, pwd)
    token = res['token_info']['token']
    # 3. 充值
    sign, timestamp = generate_sign(token, settings.SERVER_RSA_PUB_KEY)
    data = {
        'member_id': res['id'],
        'amount': 50000,
        'timestamp': timestamp,
        'sign': sign
    }
    headers = {"X-Lemonban-Media-Type": "lemonban.v3", 'Authorization': 'Bearer {}'.format(token)}
    res = send_http_request(settings.INTERFACES['recharge'], method='post', json=data, headers=headers)
    print(res.json())