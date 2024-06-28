#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：demo_led.py
@Author  ：szhu9903
@Date    ：2023/8/2 16:20 
'''
from odoo import fields, models

RELAY_ENUM = {
    'ON': 0,
    'OFF': 1,
    'AUTO': 0,
    'MANUAL': 1,

}

class Full103Relay(models.Model):
    """
    测试板设备LED控制
    """
    _name = 'full103.relay'
    _description = '开关控制'
    _rec_name = 'fr_equipcode'
    _sql_constraints = [
        ('uk_full103_relay_fr_equip_id', 'UNIQUE (fr_equip_id)', 'full103 relay fr_equip_id unique!'),
    ]

    fr_equip_id = fields.Many2one('hardware.equip', string='设备')
    fr_equipcode = fields.Integer(string='设备编码')
    fr_switch = fields.Selection([('ON', '开'), ('OFF', '关')], string='开/关')
    fr_controlmode = fields.Selection([('AUTO', '自动'), ('MANUAL', '手动')], string='控制方式')

    def write(self, vals):
        res = super(Full103Relay, self).write(vals)
        message_data = {
            'relay_switch': RELAY_ENUM[self.fr_switch],
            'relay_control': RELAY_ENUM[self.fr_controlmode],
        }
        self.env['util.rabbitmq'].send_to_equip(self.fr_equip_id.he_num, '021201', message_data)
        return res
