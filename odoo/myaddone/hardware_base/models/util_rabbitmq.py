#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：util_rabbitmq.py
@Author  ：szhu9903
@Date    ：2023/8/8 23:56 
'''

import pika
import json
import traceback
import logging
import threading
from odoo import fields, models,api

_logger = logging.getLogger(__name__)

RABBITMQ_CONFIG = {
    "rabbitmq_host": "localhost",
    "rabbitmq_port": 5672,
    "rabbitmq_virtual_host": "my_vhost",
    "rabbitmq_username": "admin",
    "rabbitmq_password": "szhu9903",
}

class UtilRabbitmq(models.AbstractModel):
    _name = 'util.rabbitmq'
    _description = 'rabbitmq服务'

    def basic_publish(self, message_data):
        """
        发布消息
        """
        try:
            connection_parameters = pika.ConnectionParameters(
                host=RABBITMQ_CONFIG['rabbitmq_host'],  # 要连接的主机名或IP地址
                port=RABBITMQ_CONFIG['rabbitmq_port'],  # 要连接的TCP端口
                virtual_host=RABBITMQ_CONFIG['rabbitmq_virtual_host'],  # 要使用的 RabbitMQ 虚拟主机
                heartbeat=0,
                credentials=pika.PlainCredentials(RABBITMQ_CONFIG['rabbitmq_username'],
                                                  RABBITMQ_CONFIG['rabbitmq_password']))
            connection = pika.BlockingConnection(connection_parameters)
            channel = connection.channel()
            # 声明队列， 不存在会自动创建
            channel.queue_declare(queue='demo_queue', durable=True)
            # 发送消息
            channel.basic_publish(exchange='',  # 要发布到的交换机
                                  routing_key='demo_queue',  # 队列名称
                                  body=message_data,
                                  properties=pika.BasicProperties(
                                      delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                  ))
            _logger.info(f"在demo_queue发布消息：{message_data}")
        except Exception as Err:
            _logger.error(
                f"在demo_queue发布消息：{message_data}异常：{traceback.format_exc()}")

    def send_to_all_equip(self, event_no, message_data):
        message_body = {
            'MODE': 'ALL',  # 发送模式 ALL：全部设备 TYPE：分类下所有设备 SINGLE：单一按照指令编码
            'EQUIP_TYPE': '',  # 设备分类，只有mode为TYPE模式时有效
            'EQUIP_NO': '',  # 设备编码， 只有mode为SINGLE模式时有效
            'EVENT_NO': event_no,  # 指令编码
            'DATA': message_data
        }
        message_data = json.dumps(message_body)
        self.basic_publish(message_data)

    def send_to_type_equip(self, equip_type, event_no, message_data):
        message_body = {
            'MODE': 'TYPE',  # 发送模式 ALL：全部设备 TYPE：分类下所有设备 SINGLE：单一按照指令编码
            'EQUIP_TYPE': equip_type,  # 设备分类，只有mode为TYPE模式时有效
            'EQUIP_NO': '',  # 设备编码， 只有mode为SINGLE模式时有效
            'EVENT_NO': event_no,  # 指令编码
            'DATA': message_data
        }
        message_data = json.dumps(message_body)
        self.basic_publish(message_data)

    def send_to_equip(self, equip_no, event_no, message_data):
        message_body = {
            'MODE': 'SINGLE',  # 发送模式 ALL：全部设备 TYPE：分类下所有设备 SINGLE：单一按照指令编码
            'EQUIP_TYPE': '',  # 设备分类，只有mode为TYPE模式时有效
            'EQUIP_NO': equip_no,  # 设备编码， 只有mode为SINGLE模式时有效
            'EVENT_NO': event_no,  # 指令编码
            'DATA': message_data
        }
        send_data = json.dumps(message_body)
        self.basic_publish(send_data)

    def call_back(self, ch, method, properties, body):
        try:
            body_dict = json.loads(body)
            event_no = body_dict['EVENT_NO']
            _logger.info('ack ok event_no=%s' % event_no)
            with self.pool.cursor() as cr:
                new_self = self.with_env(self.env(cr=cr))
                new_self.env.user.notify_success(message=f'ack ({event_no}) ok')
                # new_self.commit()

        except Exception as Err:
            traceback.print_exc()
            _logger.error(f'down message error :{str(Err)}')
        finally:
            # 发送ack
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def get_client(self):
        """返回rabbitmq客户端"""
        try:
            connection_parameters = pika.ConnectionParameters(
                host=RABBITMQ_CONFIG['rabbitmq_host'],  # 要连接的主机名或IP地址
                port=RABBITMQ_CONFIG['rabbitmq_port'],  # 要连接的TCP端口
                virtual_host=RABBITMQ_CONFIG['rabbitmq_virtual_host'],  # 要使用的 RabbitMQ 虚拟主机
                credentials=pika.PlainCredentials(RABBITMQ_CONFIG['rabbitmq_username'],
                                                  RABBITMQ_CONFIG['rabbitmq_password']),  # 身份验证
            )
            # 创建连接
            connection = pika.BlockingConnection(connection_parameters)
            # 创建连接内通道
            channel = connection.channel()
            # 声明队列， 不存在会自动创建
            channel.queue_declare(queue='ack_queue', durable=True)
            # 接收消息，设置公平模式，当消费者ACK，rabbitMQ再发送下一条消息
            channel.basic_qos(prefetch_count=1)
            # 接收消息
            channel.basic_consume(queue='ack_queue',
                                        on_message_callback=self.call_back,
                                        auto_ack=False)
            return channel
        except Exception as err:
            _logger.error(f"创建RabbimtMq客户端失败:{traceback.format_exc()}")

    def run(self):
        try:
            channel = self.get_client()
            _logger.info(f"运行rabbit server")
            t = threading.Thread(target=channel.start_consuming)
            t.setDaemon(True)
            t.start()
        except Exception as err:
            _logger.error(f"启动线程失败：{traceback.format_exc()}")
