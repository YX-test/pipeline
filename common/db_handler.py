#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 21:22
# @Author : 心蓝
import pymysql
from pymysql.cursors import DictCursor


class SQLdbHandler:
    """
    sql数据库查询类
    """
    def __init__(self, db_config):
        # 创建连接
        # 根据不同的数据库，创建不同的链接
        engine = db_config.pop('engine', 'mysql')
        if engine.lower() == 'mysql':
            self.conn = pymysql.connect(**db_config)

    def get_one(self, sql, res_type='t'):
        """
        获取一条数据
        :param sql:
        :param res_type: 返回数据的类型 默认为't表示以元组的形式返回
                        'd'表示以字典的形式返回
        :return: 元组/字典
        """
        if res_type == 't':
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()
        else:
            with self.conn.cursor(DictCursor) as cursor:
                cursor.execute(sql)
                return cursor.fetchone()

    def get_many(self, sql, size, res_type='t'):
        """
        获取多条数据
        :param sql:
        :param size: 指定的条数
        :param res_type:
        :return:
        """
        if res_type == 't':
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchmany(size)
        else:
            with self.conn.cursor(DictCursor) as cursor:
                cursor.execute(sql)
                return cursor.fetchmany(size)

    def get_all(self, sql, res_type='t'):
        """
        获取所有数据
        :param sql:
        :param res_type:
        :return:
        """
        if res_type == 't':
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        else:
            with self.conn.cursor(DictCursor) as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

    def exist(self, sql):
        """
        查询数据是否存在
        :param sql:
        :return:
        """
        if self.get_one(sql):
            return True
        else:
            return False

    def __del__(self):
        """
        对象销毁的时候自动被调用
        :return:
        """
        self.conn.close()


if __name__ == '__main__':
    import settings
    db = SQLdbHandler(settings.DB_CONFIG)
    sql = 'select leave_amount from member where id=10000000000'
    res = db.get_one(sql, 'd')
    print(res)
    print(db.exist(sql))
