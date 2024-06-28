#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：assign_code.py
@Author  ：szhu9903
@Date    ：2023/8/14 17:36 
'''

from odoo import fields, models, api

class AssignCode(models.TransientModel):
    _name = "assign.code"
    _description = "分配编号"

    assign_code_id = fields.Many2one("hardware.equip",string="设备编号")

    @api.model
    def default_get(self, fields_list):
        res = super(AssignCode, self).default_get(fields_list)
        return res

    @api.onchange('assign_code_id')
    def _onchange_type(self):
        domain = [('he_starttype', '=', 'UNASSIGNED')]
        action_equip_type = self.env.context.get('action_equip_type', [])
        if action_equip_type:
            domain.append(('he_type_id', '=', action_equip_type))
        return {
            'domain': {'assign_code_id': domain}
        }

    def button_assign_new_code(self):
        self.ensure_one()
        action_equip_code = self.env.context.get('action_equip_code', None)
        new_assign_code = self.assign_code_id.he_num
        if action_equip_code and new_assign_code:
            send_date = {'he_num': new_assign_code}
            # 发送更新设备编号到设备
            self.env['util.rabbitmq'].send_to_equip(action_equip_code, '020003', send_date)
        return True
