#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：demo_led.py
@Author  ：szhu9903
@Date    ：2023/8/2 16:20 
'''
from odoo import fields, models

class DemoLed(models.Model):
    """
    测试板设备LED控制
    """
    _name = 'demo.led'
    _description = 'LED控制'
    _rec_name = 'dl_equipcode'
    _sql_constraints = [
        ('uk_demo_led_dl_equipid', 'UNIQUE (dl_equipid)', 'demo led dl_equipid unique!'),
    ]

    dl_equip_id = fields.Many2one('hardware.equip', '设备')
    dl_equipcode = fields.Integer('设备编码')
    dl_switch = fields.Selection([('0', '开'), ('1', '关')],'开/关')
    dl_r = fields.Integer('LED-R')
    dl_g = fields.Integer('LED-G')
    dl_b = fields.Integer('LED-B')

    def write(self, vals):
        res = super(DemoLed, self).write(vals)
        message_data = {
            'led_switch': self.dl_switch,
            'led_r': self.dl_r,
            'led_g': self.dl_g,
            'led_b': self.dl_b,
        }
        self.env['util.rabbitmq'].send_to_equip(self.dl_equip_id.he_num, '020201', message_data)
        return res
