#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：hardware_type.py
@Author  ：szhu9903
@Date    ：2023/8/2 09:06 
'''
from odoo import fields, models, api

class HardwareType(models.Model):
    """
    设备类型表
    """
    _name = 'hardware.type'
    _description = '设备类型表'
    _rec_name = 'ht_name'
    _sql_constraints = [
        ('uk_hardware_type_ht_name', 'UNIQUE (ht_name)', 'hardware type ht_name unique!'),
    ]

    ht_name = fields.Char('分类名称', required=True)
    ht_code_down = fields.Integer('编码范围下', required=True)
    ht_code_up = fields.Integer('编码范围上', required=True)

    @api.model
    def create(self, vals_list):
        res = super(HardwareType, self).create(vals_list)
        hardwareEquip = self.env['hardware.equip']
        equip_data = {
            'he_name': f'{res.ht_name}-初始设备',
            'he_num': res.ht_code_down,
            'he_type_id': res.id,
            'he_starttype': 'START',
            'he_effect': 'TEMP',
        }
        hardwareEquip.create(equip_data)
        return res

    def write(self, vals):
        before_code = self.ht_code_down
        res = super(HardwareType, self).write(vals)
        after_code = self.ht_code_down
        if before_code != after_code:
            # 获取该分类的临时设备
            temp_equip = self.env['hardware.equip'].search([('he_num', '=', before_code)])
            if temp_equip:
                temp_equip.he_num = after_code
                temp_equip.he_starttype = 'START'
                temp_equip.he_effect = 'TEMP'
        return res