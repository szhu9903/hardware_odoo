#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：hardware_equip.py
@Author  ：szhu9903
@Date    ：2023/8/2 09:04 
'''

import asyncio
import time
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HardwareEquip(models.Model):
    _name = 'hardware.equip'
    _description = '设备表'
    _rec_name = 'he_name'
    _sql_constraints = [
        ('uk_hardware_equip_he_num', 'UNIQUE (he_num)', 'equip he_num unique!'),
    ]

    he_name = fields.Char('设备名称', required=True)
    he_num = fields.Integer('设备编号', required=True)
    he_type_id = fields.Many2one('hardware.type', string='设备分类', required=True)
    he_equipstatus = fields.Selection([('BROKEN', '离线'), ('LINKED', '在线')], '登录状态', default='BROKEN')
    he_starttype = fields.Selection([('START', '启用'), ('STOP', '停用'), ('UNASSIGNED', '待分配')], '设备状态', default='UNASSIGNED')
    he_effect = fields.Selection([('TEMP', '临时设备'), ('NORMAL', '正常设备')], '设备作用', default='NORMAL')

    @api.model
    def create(self, vals_list):
        he_type_data = self.env['hardware.type'].browse(vals_list['he_type_id'])
        if he_type_data.ht_code_down <= vals_list['he_num'] < he_type_data.ht_code_up:
            res = super(HardwareEquip, self).create(vals_list)
            return res
        raise ValidationError('he_num not in hardware code scope!')

    def write(self, vals):
        res = super(HardwareEquip, self).write(vals)
        return res

    def unlink(self):
        res = super(HardwareEquip, self).unlink()
        return res

    @api.constrains('he_num', 'he_type_id')
    def _constraint_he_num_he_type(self):
        for equip in self:
            if equip.he_type_id.ht_code_down <= equip.he_num < equip.he_type_id.ht_code_up:
                return
            raise ValidationError('he_num not in hardware code scope!')

    # 页面he_num变化确认时直接触发
    @api.onchange('he_num')
    def _onchange_he_num(self):
        if not self.he_num: return
        hardwre_type = self.env['hardware.type'].search([])
        for h_type in hardwre_type:
            if h_type.ht_code_down <= self.he_num < h_type.ht_code_up:
                self.he_type_id = h_type
                return
        return {
            "warning": {
                "title": "编号错误",
                "message": "设备编码不在任何范围内！",
            }
        }


    # def button_point_code(self):
    #     formview_ref = self.env.ref('hardware_base.hardware_base.hardware_equip_form_view',False)
    #     treeview_ref = self.env.ref('hardware_base.hardware_base.hardware_equip_tree_view',False)
    #     return {
    #         'name': '分配设备',
    #         'view_type': 'form',
    #         'view_model': 'form,tree',
    #         'res_model': 'hardware.equip',
    #         'domain':"[(1,'=',1)]",
    #         'views':[(treeview_ref and treeview_ref.id or False,'tree'),
    #                  (formview_ref and formview_ref.id or False,'form')],
    #         'type':'ir.actions.act_window',
    #         'target':'new'
    #     }
