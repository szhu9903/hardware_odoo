#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：demo_env.py
@Author  ：szhu9903
@Date    ：2023/8/2 10:41 
'''

from odoo import fields, models

class Full103Env(models.Model):
    """
    测试板设备环境数据
    """
    _name = 'full103.env'
    _description = '环境数据'
    _rec_name = 'fe_equipcode'
    _sql_constraints = [
        ('uk_full103_env_fe_equip_id', 'UNIQUE (fe_equip_id)', 'full103 env fe_equip_id unique!'),
    ]

    fe_equip_id = fields.Many2one('hardware.equip', string='设备')
    fe_equipcode = fields.Integer(string='设备编码')
    fe_temperature = fields.Float(string='温度', digits=(5, 2))
    fe_humidity = fields.Float(string='湿度', digits=(5, 2))
    last_modify_time = fields.Datetime(string='更新时间', default=lambda self: fields.Datetime.now())

    def button_update_env(self):
        """
        1. 发送消息到硬件
        2. 异步检测硬件响应情况
        """
        # 更新响应消息配置 为等待状态
        self.env['util.rabbitmq'].send_to_equip(1002, '011102', {})

