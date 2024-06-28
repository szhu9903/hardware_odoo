#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：hardware_tcp_server_pgsql 
@File    ：pgsql_db.py
@Author  ：szhu9903
@Date    ：2023/8/10 17:15 
'''

import threading
import psycopg2
import traceback
from psycopg2.extras import RealDictCursor

from collections import deque
from twisted.python import log
from config import thread_data, PgsqlConf

class PgsqlPool():
    """
    postgresql 连接池
    """
    __connection_pool = deque(maxlen=10)
    pool_mutex = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """初始化数据库连接队列"""
        for i in range(10):
            connection = psycopg2.connect(host=PgsqlConf.host,
                                          port=PgsqlConf.port,
                                          user=PgsqlConf.user,
                                          password=PgsqlConf.password,
                                          database=PgsqlConf.db_name)
            cls.__connection_pool.append(connection)
        super(PgsqlPool, cls).__new__(cls)

    @classmethod
    def get_idle_connection(cls):
        """ 获取空闲连接 """
        idle_connection = None
        try:
            cls.pool_mutex.acquire()
            idle_connection = cls.__connection_pool.pop()
        except Exception as Err:
            log.err('err:', str(Err))
        finally:
            cls.pool_mutex.release()
        return idle_connection

    @classmethod
    def resume_idle_connection(cls, used_connection):
        """ 返回空闲连接 """
        try:
            cls.pool_mutex.acquire()
            cls.__connection_pool.appendleft(used_connection)
        except Exception as Err:
            log.err('release err:', str(Err))
        finally:
            cls.pool_mutex.release()

    @staticmethod
    def insert_data_db(insert_sql, params=None):
        """插入数据库"""
        result = False
        last_id = 0
        for tries_times in range(3):
            cursor = thread_data.connection.cursor()
            try:
                cursor.execute(insert_sql, params)
                last_id = cursor.lastrowid
                result = True

                thread_data.connection.commit()
                cursor.close()
                break
            except Exception as Err:
                if tries_times == 2:
                    log.err('CommFunc:Error in DB Execute(%s):%s' % (insert_sql, str(Err)))
                    traceback.print_exc()
                cursor.close()
        return result, last_id

    @staticmethod
    def query_data_db(query_sql, params=None):
        """ 查询数据库数据集 """
        result = None
        for tries_times in range(3):
            cursor = thread_data.connection.cursor(cursor_factory=RealDictCursor)
            try:
                cursor.execute(query_sql, params)
                res = cursor.fetchall()
                result = [dict(r) for r in res]
                cursor.close()
                break
            except Exception as Err:
                if tries_times == 2:
                    log.err('CommFunc:Error in DB Execute(%s):%s' % (query_sql, str(Err)))
                    traceback.print_exc()
                cursor.close()
        return result

# if __name__ == '__main__':
#     PgsqlPool()

