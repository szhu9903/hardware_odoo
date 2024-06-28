#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：twisted_server 
@File    ：config.py
@Author  ：szhu9903
@Date    ：2022/11/17 14:17 
'''

import threading

# 线程会话变量,隔离数据库链接
thread_data = threading.local()

# 系统变量
sys_config = {
    'protocols': {}, # 链接中的节点
    'last_stamp': None, # 服务起始时间
    'equip_type': {},
}

# 响应消息保存时间
REDIS_ACK_SAVE_TIME = 30

# postgresql 连接配置
class PgsqlConf():
    host     = '127.0.0.1'
    user     = 'hardware'
    password = 'hardware'
    port     = 5432
    db_name  = 'hardware_db'

class RabbitConf():
    username     = 'admin'
    password     = 'szhu9903'
    host         = 'localhost'
    port         =  5672
    virtual_host = 'my_vhost'

# rabbitmq 连接
# class RabbitConf():
#     username     = 'admin'
#     password     = 'szhu9903'
#     host         = '101.34.60.64'
#     port         =  5672
#     virtual_host = 'my_vhost'

# redis 连接
class RedisConf():
    host         = '101.34.60.64'
    port         = 6379
    password     = 'qq1017'
    db           = 6

