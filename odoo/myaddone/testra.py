#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：testra.py
@Author  ：szhu9903
@Date    ：2023/8/9 16:22 
'''

import pika


def main():
    # 身份认证实例
    credentials = pika.PlainCredentials('admin', 'szhu9903')
    # 在构造链接时传递给连接适配器连接参数的实例。
    connection_parameters = pika.ConnectionParameters(
        host='localhost',  # 要连接的主机名或IP地址
        port=5672,  # 要连接的TCP端口
        virtual_host='my_vhost',  # 要使用的 RabbitMQ 虚拟主机
        credentials=credentials,  # 身份验证
    )
    # 创建连接
    connection = pika.BlockingConnection(connection_parameters)

    # 创建连接内通道
    channel = connection.channel()

    # 定义消息处理程序
    def callback_func(channel, method, properties, body):
        print('接收到消息：', body.decode('utf-8'))

    # 接收消息
    channel.basic_consume(queue='demo_queue',  # 接收指定queue的消息
                          on_message_callback=callback_func,  # 接收到消息后的回调函数
                          auto_ack=True)  # 是否自动发送确认消息
    print('-------------开始接收消息-----------------')

    # 开始循环等待，一直处于等待接收消息的状态
    channel.start_consuming()

if __name__ == '__main__':
    main()