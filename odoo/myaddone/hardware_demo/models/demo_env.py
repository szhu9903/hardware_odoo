#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：demo_env.py
@Author  ：szhu9903
@Date    ：2023/8/2 10:41 
'''

from odoo import fields, models

class DemoEnv(models.Model):
    """
    测试板设备环境数据
    """
    _name = 'demo.env'
    _description = '环境数据'
    _rec_name = 'de_equipcode'
    _sql_constraints = [
        ('uk_demo_env_de_equip_id', 'UNIQUE (de_equip_id)', 'demo env de_equipid unique!'),
    ]

    de_equip_id = fields.Many2one('hardware.equip', '设备')
    de_equipcode = fields.Integer('设备编码')
    de_temperature = fields.Float('温度', digits=(5, 2))
    de_humidity = fields.Float('湿度', digits=(5, 2))
    last_modify_time = fields.Datetime(string='更新时间', default=lambda self: fields.Datetime.now())

    def button_update_env(self):
        """
        1. 发送消息到硬件
        2. 异步检测硬件响应情况
        """
        # 更新响应消息配置 为等待状态
        self.env['util.rabbitmq'].send_to_equip(1001, '010302', {})

