#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/16 19:30
# @Author : 心蓝

import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(name, filename, encoding='utf-8', fmt=None, when='d', interval=1, backup_count=7, debug=False):
    """

    :param name: 日志器的名字
    :param filename: 日志文件名(包含路径)
    :param encoding: 字符编码
    :param fmt: 日志格式
    :param when: 日志轮转时间单位
    :param interval: 间隔
    :param backup_count: 日志文件个数
    :param debug: 调试模式
    :return:
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # 文件处理器的等级一般情况一定比控制台要高
    if debug:
        file_level = logging.DEBUG
        console_level = logging.DEBUG
    else:
        file_level = logging.WARNING
        console_level = logging.INFO

    if fmt is None:
        fmt = '%(levelname)s %(asctime)s [%(filename)s-->line:%(lineno)d]:%(message)s'

    file_handler = TimedRotatingFileHandler(
        filename=filename, when=when, interval=interval, backupCount=backup_count, encoding=encoding)
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    formatter = logging.Formatter(fmt=fmt)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    import settings
    log = get_logger(**settings.LOG_CONFIG)
    log.info('我是普通信息')
    log.warning('我是警告信息')


